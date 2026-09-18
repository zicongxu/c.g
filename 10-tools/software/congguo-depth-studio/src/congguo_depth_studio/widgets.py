from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QProcess, QSize, Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent, QMovie, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}


class BrandHeader(QFrame):
    def __init__(self, helper_path: Path, processing_path: Path) -> None:
        super().__init__()
        self.setObjectName("brandHeader")
        self.setAccessibleName("葱果深度工坊")
        # Prevent the page layout from stretching or compressing this card.
        # Its mascot is deliberately smaller than the card's inner height.
        self.setFixedHeight(132)

        row = QHBoxLayout(self)
        row.setContentsMargins(20, 10, 12, 10)
        row.setSpacing(16)

        copy = QVBoxLayout()
        copy.setSpacing(5)
        eyebrow = QLabel("葱果实验室 · DEPTH STUDIO")
        eyebrow.setObjectName("brandEyebrow")
        self.title_label = QLabel("把动作，变成深度")
        self.title_label.setObjectName("brandTitle")
        self.subtitle_label = QLabel(
            "把视频交给葱果，远近、轮廓和动作会变成一张张深度白模。"
        )
        self.subtitle_label.setObjectName("brandSubtitle")
        self.subtitle_label.setWordWrap(True)
        privacy = QLabel("● 本地离线处理 · 视频不会上传")
        privacy.setObjectName("privacyPill")
        copy.addWidget(eyebrow)
        copy.addWidget(self.title_label)
        copy.addWidget(self.subtitle_label)
        copy.addSpacing(5)
        copy.addWidget(privacy, 0, Qt.AlignmentFlag.AlignLeft)
        copy.addStretch(1)
        row.addLayout(copy, 1)

        self.mascot_label = QLabel()
        self.mascot_label.setObjectName("mascotFrame")
        self.mascot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mascot_label.setFixedSize(112, 112)
        row.addWidget(self.mascot_label)

        self.static_pixmap = QPixmap(str(helper_path)).scaled(
            106,
            106,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.processing_movie = QMovie(str(processing_path))
        self.processing_movie.setScaledSize(QSize(63, 106))
        self.set_state("idle")

    def set_state(self, state: str) -> None:
        messages = {
            "idle": (
                "把动作，变成深度",
                "把视频交给葱果，远近、轮廓和动作会变成一张张深度白模。",
            ),
            "selected": (
                "视频收到啦",
                "检查一下输出设置，然后让葱果开始工作。",
            ),
            "processing": (
                "葱果正在观察每一帧…",
                "正在分辨角色轮廓、空间远近和镜头运动，请稍等。",
            ),
            "completed": (
                "深度视频做好啦！",
                "成片已经收进“最近输出”，可以直接播放或定位文件。",
            ),
            "error": (
                "这里好像卡住了",
                "请查看下面的错误提示，换一个视频后也可以重新尝试。",
            ),
        }
        title, subtitle = messages.get(state, messages["idle"])
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        if state == "processing" and self.processing_movie.isValid():
            self.mascot_label.clear()
            self.mascot_label.setMovie(self.processing_movie)
            self.processing_movie.start()
        else:
            self.processing_movie.stop()
            self.mascot_label.clear()
            self.mascot_label.setPixmap(self.static_pixmap)


class StageBar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("stageBar")
        self.labels: list[QLabel] = []
        row = QHBoxLayout(self)
        row.setContentsMargins(4, 0, 4, 0)
        row.setSpacing(8)
        stages = ("1  选择视频", "2  调整设置", "3  生成深度")
        for index, text in enumerate(stages, start=1):
            label = QLabel(text)
            label.setObjectName("stagePill")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setAccessibleName(f"步骤 {text}")
            self.labels.append(label)
            row.addWidget(label, 1)
            if index < 3:
                arrow = QLabel("›")
                arrow.setObjectName("stageArrow")
                row.addWidget(arrow)
        self.set_stage(1)

    def set_stage(self, stage: int, finished: bool = False) -> None:
        for index, label in enumerate(self.labels, start=1):
            if index < stage or (finished and index == stage):
                state = "complete"
            elif index == stage:
                state = "current"
            else:
                state = "upcoming"
            label.setProperty("state", state)
            label.style().unpolish(label)
            label.style().polish(label)


class DropArea(QFrame):
    file_selected = Signal(Path)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dropArea")
        self.setProperty("active", False)
        self.setProperty("selected", False)
        self.setAcceptDrops(True)
        self.setMinimumHeight(116)
        self.setAccessibleName("视频拖放区域，尚未选择视频")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(7)

        self.state_label = QLabel("选择输入视频")
        self.state_label.setObjectName("dropEyebrow")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel("拖入视频，或点击下方按钮选择")
        self.title_label.setObjectName("dropTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label = QLabel("支持 MP4、MOV、M4V、AVI、MKV 和 WebM")
        self.hint_label.setObjectName("secondary")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.state_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.hint_label)

    def set_selected(self, path: Path, width: int, height: int, duration: float) -> None:
        self.setProperty("selected", True)
        self.state_label.setText("✓ 已选择视频")
        self.title_label.setText(path.name)
        self.hint_label.setText(
            f"{width}×{height}  ·  {duration:.1f} 秒  ·  再次拖入可替换"
        )
        self.setToolTip(str(path))
        self.setAccessibleName(f"已选择视频：{path.name}")
        self._refresh_style()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        urls = event.mimeData().urls()
        if urls and Path(urls[0].toLocalFile()).suffix.lower() in VIDEO_EXTENSIONS:
            event.acceptProposedAction()
            self._set_active(True)

    def dragLeaveEvent(self, event) -> None:
        self._set_active(False)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        self._set_active(False)
        urls = event.mimeData().urls()
        if urls:
            self.file_selected.emit(Path(urls[0].toLocalFile()))
            event.acceptProposedAction()

    def _set_active(self, active: bool) -> None:
        self.setProperty("active", active)
        self._refresh_style()

    def _refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)


class ResultItem(QFrame):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.setObjectName("resultItem")
        self.setToolTip(str(path))
        self.setAccessibleName(f"已完成的深度视频：{path.name}")

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 11, 12, 11)
        row.setSpacing(12)

        status = QLabel("✓")
        status.setObjectName("resultStatus")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setFixedSize(28, 28)
        row.addWidget(status)

        text = QVBoxLayout()
        text.setSpacing(3)
        name = QLabel(path.name)
        name.setObjectName("resultTitle")
        meta = QLabel(self._metadata(path))
        meta.setObjectName("secondary")
        meta.setToolTip(str(path.parent))
        text.addWidget(name)
        text.addWidget(meta)
        row.addLayout(text, 1)

        play = QPushButton("播放")
        play.setAccessibleName(f"播放 {path.name}")
        play.clicked.connect(self.open_video)
        locate = QPushButton("定位")
        locate.setAccessibleName(f"在文件管理器中定位 {path.name}")
        locate.clicked.connect(self.reveal_video)
        row.addWidget(play)
        row.addWidget(locate)

    @staticmethod
    def _metadata(path: Path) -> str:
        try:
            stat = path.stat()
            size = stat.st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%m-%d %H:%M")
            return f"{size:.1f} MB  ·  {modified}  ·  {path.parent.name}"
        except OSError:
            return str(path.parent)

    def open_video(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path)))

    def reveal_video(self) -> None:
        if sys.platform == "darwin":
            QProcess.startDetached("/usr/bin/open", ["-R", str(self.path)])
        elif sys.platform == "win32":
            QProcess.startDetached("explorer.exe", ["/select,", str(self.path)])
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path.parent)))


class ResultsPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("resultsPanel")
        self.setAccessibleName("最近输出")
        self._paths: list[Path] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 10, 16, 10)
        outer.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("最近输出")
        title.setObjectName("sectionTitle")
        self.count_label = QLabel("0 个")
        self.count_label.setObjectName("secondary")
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(self.count_label)
        outer.addLayout(header)

        self.empty_label = QLabel(
            "处理完成的视频会显示在这里，可直接播放或定位文件。"
        )
        self.empty_label.setObjectName("secondary")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setMinimumHeight(38)
        outer.addWidget(self.empty_label)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("resultsScroll")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setMaximumHeight(156)
        self.scroll.setVisible(False)
        container = QWidget()
        container.setObjectName("resultsContainer")
        self.items_layout = QVBoxLayout(container)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(8)
        self.items_layout.addStretch(1)
        self.scroll.setWidget(container)
        outer.addWidget(self.scroll)

    def add_result(self, path: Path) -> None:
        resolved = path.resolve()
        if resolved in self._paths:
            index = self._paths.index(resolved)
            self._paths.pop(index)
            item = self.items_layout.takeAt(index).widget()
            if item:
                item.deleteLater()
        self._paths.insert(0, resolved)
        self.items_layout.insertWidget(0, ResultItem(resolved))
        while len(self._paths) > 8:
            self._paths.pop()
            item = self.items_layout.takeAt(self.items_layout.count() - 2).widget()
            if item:
                item.deleteLater()
        self.empty_label.setVisible(False)
        self.scroll.setVisible(True)
        self.count_label.setText(f"{len(self._paths)} 个")

    @property
    def paths(self) -> list[Path]:
        return list(self._paths)
