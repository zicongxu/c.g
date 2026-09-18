from __future__ import annotations

import os
import sys
import threading
from pathlib import Path

from PySide6.QtCore import QObject, QSettings, Qt, QThread, Signal, Slot
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .depth_processor import DepthProcessor, ProcessingCancelled, probe_video
from .styles import APP_STYLE
from .widgets import BrandHeader, DropArea, ResultsPanel, StageBar


def resource_path(name: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "resources" / name
    return Path(__file__).resolve().parent / "resources" / name


class ProcessingWorker(QObject):
    progress = Signal(int, str, object)
    succeeded = Signal(Path)
    failed = Signal(str)
    cancelled = Signal()
    done = Signal()

    def __init__(self, source: Path, target: Path, model: Path, fps: int, audio: bool):
        super().__init__()
        self.source = source
        self.target = target
        self.model = model
        self.fps = fps
        self.audio = audio
        self._cancel = threading.Event()

    @Slot()
    def run(self) -> None:
        try:
            processor = DepthProcessor(
                self.model,
                lambda value, message, eta: self.progress.emit(value, message, eta),
                self._cancel.is_set,
            )
            processor.run(self.source, self.target, self.fps, self.audio)
            self.succeeded.emit(self.target)
        except ProcessingCancelled:
            self.cancelled.emit()
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            self.done.emit()

    def request_cancel(self) -> None:
        self._cancel.set()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.source_path: Path | None = None
        self.output_path: Path | None = None
        self.thread: QThread | None = None
        self.worker: ProcessingWorker | None = None
        self.settings = QSettings("Local Depth Tools", "Depth Motion Studio")
        self.model_path = resource_path("depth_anything_v2_vits.onnx")

        self.setWindowTitle("葱果深度工坊")
        # Keep the first launch inside the screen's usable area. The page itself
        # scrolls when a small display or a large Dock leaves less room.
        available = QApplication.primaryScreen().availableGeometry()
        self.setMinimumSize(680, 600)
        self.resize(min(900, available.width() - 32), min(760, available.height() - 32))
        self._build_ui()
        self._check_ready()
        self._load_recent_outputs()

    def _build_ui(self) -> None:
        page_scroll = QScrollArea()
        page_scroll.setObjectName("pageScroll")
        page_scroll.setWidgetResizable(True)
        page_scroll.setFrameShape(QFrame.Shape.NoFrame)
        page_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(page_scroll)

        root = QWidget()
        root.setObjectName("root")
        page_scroll.setWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(20, 16, 20, 18)
        main.setSpacing(10)

        self.brand_header = BrandHeader(
            resource_path("brand/cong-guo-depth-helper.png"),
            resource_path("brand/cong-guo-processing.gif"),
        )
        main.addWidget(self.brand_header)

        self.stage_bar = StageBar()
        main.addWidget(self.stage_bar)

        self.drop_area = DropArea()
        self.drop_area.file_selected.connect(self.set_source)
        main.addWidget(self.drop_area)

        source_row = QHBoxLayout()
        self.source_label = QLabel("尚未选择视频")
        self.source_label.setObjectName("secondary")
        self.source_label.setWordWrap(True)
        self.choose_button = QPushButton("选择视频")
        self.choose_button.setAccessibleName("选择输入视频")
        self.choose_button.clicked.connect(self.choose_source)
        source_row.addWidget(self.source_label, 1)
        source_row.addWidget(self.choose_button)
        main.addLayout(source_row)

        options = QFrame()
        options.setObjectName("panel")
        options_layout = QVBoxLayout(options)
        options_layout.setContentsMargins(18, 16, 18, 16)
        options_layout.setSpacing(12)

        setting_row = QHBoxLayout()
        setting_row.addWidget(QLabel("输出帧率"))
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["24 FPS", "30 FPS", "60 FPS"])
        self.fps_combo.setCurrentIndex(1)
        self.fps_combo.setAccessibleName("输出帧率")
        setting_row.addWidget(self.fps_combo)
        setting_row.addSpacing(18)
        self.audio_check = QCheckBox("保留原始音频")
        self.audio_check.setChecked(True)
        setting_row.addWidget(self.audio_check)
        setting_row.addStretch(1)
        options_layout.addLayout(setting_row)

        output_row = QHBoxLayout()
        output_row.addWidget(QLabel("保存到"))
        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("选择视频后自动生成")
        self.output_edit.setAccessibleName("输出文件位置")
        self.output_button = QPushButton("更改…")
        self.output_button.clicked.connect(self.choose_output)
        output_row.addWidget(self.output_edit, 1)
        output_row.addWidget(self.output_button)
        options_layout.addLayout(output_row)
        main.addWidget(options)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setAccessibleName("处理进度")
        main.addWidget(self.progress)

        status_row = QHBoxLayout()
        self.status_label = QLabel("正在检查运行环境…")
        self.status_label.setObjectName("secondary")
        self.eta_label = QLabel("")
        self.eta_label.setObjectName("secondary")
        status_row.addWidget(self.status_label, 1)
        status_row.addWidget(self.eta_label)
        main.addLayout(status_row)

        button_row = QHBoxLayout()
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("danger")
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.start_button = QPushButton("开始提取深度")
        self.start_button.setObjectName("primary")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_processing)
        button_row.addStretch(1)
        button_row.addWidget(self.cancel_button)
        button_row.addWidget(self.start_button)
        main.addLayout(button_row)

        self.results_panel = ResultsPanel()
        main.addWidget(self.results_panel)

    def _check_ready(self) -> None:
        if not self.model_path.exists():
            self.status_label.setText("运行环境异常：内置深度模型缺失")
            self.brand_header.set_state("error")
            return
        self.status_label.setText("准备就绪 · 把视频拖给葱果吧")
        self.brand_header.set_state("idle")
        self.stage_bar.set_stage(1)

    @Slot()
    def choose_source(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频",
            str(Path.home()),
            "视频文件 (*.mp4 *.mov *.m4v *.avi *.mkv *.webm)",
        )
        if path:
            self.set_source(Path(path))

    @Slot(Path)
    def set_source(self, path: Path) -> None:
        try:
            info = probe_video(path)
        except Exception as exc:
            QMessageBox.warning(self, "无法读取视频", str(exc))
            return
        self.source_path = path
        duration = float(info["duration"])
        self.drop_area.set_selected(
            path, int(info["width"]), int(info["height"]), duration
        )
        self.source_label.setText(f"输入位置：{path.parent}")
        self.source_label.setToolTip(str(path))
        self.choose_button.setText("更换视频")
        self.output_path = path.with_name(f"{path.stem}_depth.mp4")
        self.output_edit.setText(str(self.output_path))
        self.start_button.setEnabled(self.model_path.exists())
        self.status_label.setText("视频已就绪")
        self.progress.setValue(0)
        self.brand_header.set_state("selected")
        self.stage_bar.set_stage(2)

    @Slot()
    def choose_output(self) -> None:
        default = str(self.output_path or (Path.home() / "depth_video.mp4"))
        path, _ = QFileDialog.getSaveFileName(
            self, "保存深度视频", default, "MP4 视频 (*.mp4)"
        )
        if path:
            self.output_path = Path(path if path.lower().endswith(".mp4") else f"{path}.mp4")
            self.output_edit.setText(str(self.output_path))

    @Slot()
    def start_processing(self) -> None:
        if not self.source_path or not self.output_path:
            return
        if self.output_path.exists():
            answer = QMessageBox.question(
                self, "覆盖文件？", "输出文件已经存在，是否覆盖？"
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        fps = int(self.fps_combo.currentText().split()[0])
        self.worker = ProcessingWorker(
            self.source_path, self.output_path, self.model_path, fps, self.audio_check.isChecked()
        )
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress)
        self.worker.succeeded.connect(self.on_success)
        self.worker.failed.connect(self.on_failure)
        self.worker.cancelled.connect(self.on_cancelled)
        self.worker.done.connect(self.thread.quit)
        self.thread.finished.connect(self._thread_finished)
        self._set_running(True)
        self.brand_header.set_state("processing")
        self.stage_bar.set_stage(3)
        self.thread.start()

    @Slot(int, str, object)
    def on_progress(self, value: int, message: str, eta: object) -> None:
        self.progress.setValue(value)
        self.status_label.setText(message)
        has_eta = isinstance(eta, (int, float)) and eta
        self.eta_label.setText(self._format_eta(eta) if has_eta else "")

    @Slot(Path)
    def on_success(self, path: Path) -> None:
        self.progress.setValue(100)
        self.status_label.setText("处理完成 · 已加入最近输出")
        self.eta_label.clear()
        self.results_panel.add_result(path)
        self._remember_result(path)
        self.results_panel.setFocus(Qt.FocusReason.OtherFocusReason)
        self.brand_header.set_state("completed")
        self.stage_bar.set_stage(3, finished=True)

    @Slot(str)
    def on_failure(self, message: str) -> None:
        self.progress.setValue(0)
        self.status_label.setText("处理失败")
        self.brand_header.set_state("error")
        QMessageBox.critical(self, "处理失败", message)

    @Slot()
    def on_cancelled(self) -> None:
        self.progress.setValue(0)
        self.status_label.setText("已取消")
        self.eta_label.clear()
        self.brand_header.set_state("selected")
        self.stage_bar.set_stage(2)

    @Slot()
    def cancel_processing(self) -> None:
        if self.worker:
            self.worker.request_cancel()
            self.cancel_button.setEnabled(False)
            self.status_label.setText("正在取消…")

    @Slot()
    def _thread_finished(self) -> None:
        self._set_running(False)
        if self.worker:
            self.worker.deleteLater()
        if self.thread:
            self.thread.deleteLater()
        self.worker = None
        self.thread = None

    def _set_running(self, running: bool) -> None:
        self.start_button.setVisible(not running)
        self.cancel_button.setVisible(running)
        self.cancel_button.setEnabled(True)
        self.fps_combo.setEnabled(not running)
        self.audio_check.setEnabled(not running)
        self.drop_area.setEnabled(not running)
        self.choose_button.setEnabled(not running)
        self.output_button.setEnabled(not running)

    def _load_recent_outputs(self) -> None:
        stored = self.settings.value("recentOutputs", [])
        if isinstance(stored, str):
            stored = [stored]
        existing = [Path(value) for value in stored if Path(value).exists()]
        for path in reversed(existing[:8]):
            self.results_panel.add_result(path)
        if len(existing) != len(stored):
            self.settings.setValue("recentOutputs", [str(path) for path in existing[:8]])

    def _remember_result(self, path: Path) -> None:
        values = [str(item) for item in self.results_panel.paths[:8]]
        self.settings.setValue("recentOutputs", values)

    @staticmethod
    def _format_eta(seconds: float) -> str:
        seconds = max(0, int(seconds))
        if seconds < 60:
            return f"约 {seconds} 秒"
        return f"约 {seconds // 60} 分 {seconds % 60} 秒"

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.thread and self.thread.isRunning():
            answer = QMessageBox.question(
                self, "退出应用？", "深度视频仍在处理中，确定退出吗？"
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            if self.worker:
                self.worker.request_cancel()
            self.thread.quit()
            self.thread.wait(3000)
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("葱果深度工坊")
    app.setOrganizationName("葱果")
    app.setWindowIcon(QIcon(str(resource_path("brand/cong-guo-app-icon.png"))))
    app.setStyleSheet(APP_STYLE)
    window = MainWindow()
    if os.environ.get("DEPTH_STUDIO_SMOKE_TEST") == "1":
        # Keep the packaging probe ASCII-only: Windows CI may use a legacy console
        # code page even though the actual GUI renders Unicode normally.
        print(f"ready={window.model_path.exists()}")
        return 0
    test_input = os.environ.get("DEPTH_STUDIO_PROCESS_TEST_INPUT")
    test_output = os.environ.get("DEPTH_STUDIO_PROCESS_TEST_OUTPUT")
    if test_input and test_output:
        processor = DepthProcessor(
            window.model_path,
            lambda value, message, eta: print(value, message, eta or ""),
            lambda: False,
        )
        processor.run(Path(test_input), Path(test_output), 24, True)
        print(f"output={test_output}")
        return 0
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
