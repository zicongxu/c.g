from __future__ import annotations

import sys
import threading
from datetime import datetime
from pathlib import Path

import cv2
from PySide6.QtCore import (
    QObject,
    QPointF,
    QProcess,
    QRunnable,
    QSize,
    Qt,
    QThreadPool,
    QUrl,
    Signal,
    Slot,
)
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QDragEnterEvent,
    QDropEvent,
    QImage,
    QMovie,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
)
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
_THUMBNAIL_CACHE: dict[Path, QImage] = {}
_THUMBNAIL_CACHE_LOCK = threading.Lock()


def extract_video_thumbnail(path: Path) -> QImage:
    """Decode a representative frame without touching the UI thread."""

    capture = cv2.VideoCapture(str(path))
    try:
        if not capture.isOpened():
            raise ValueError(f"无法读取视频缩略图：{path.name}")
        if hasattr(cv2, "CAP_PROP_ORIENTATION_AUTO"):
            capture.set(cv2.CAP_PROP_ORIENTATION_AUTO, 1)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count > 1:
            capture.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(frame_count * 0.12)))
        success, frame = capture.read()
        if not success and frame_count > 1:
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = capture.read()
        if not success or frame is None:
            raise ValueError(f"无法读取视频缩略图：{path.name}")
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb.shape
        return QImage(
            rgb.data,
            width,
            height,
            channels * width,
            QImage.Format.Format_RGB888,
        ).copy()
    finally:
        capture.release()


class _ThumbnailSignals(QObject):
    loaded = Signal(Path, object)
    failed = Signal(Path)


class _ThumbnailWorker(QRunnable):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.signals = _ThumbnailSignals()

    @Slot()
    def run(self) -> None:
        try:
            with _THUMBNAIL_CACHE_LOCK:
                cached = _THUMBNAIL_CACHE.get(self.path)
            image = cached or extract_video_thumbnail(self.path)
            if cached is None:
                with _THUMBNAIL_CACHE_LOCK:
                    _THUMBNAIL_CACHE[self.path] = image
        except Exception:
            self._emit_failed()
            return
        self._emit_loaded(image)

    def _emit_loaded(self, image: QImage) -> None:
        try:
            self.signals.loaded.emit(self.path, image)
        except RuntimeError:
            # The app can close before a background thumbnail finishes.
            pass

    def _emit_failed(self) -> None:
        try:
            self.signals.failed.emit(self.path)
        except RuntimeError:
            # The receiving UI object has already been destroyed.
            pass


class VideoThumbnail(QLabel):
    activated = Signal()

    def __init__(self, width: int, height: int, interactive: bool = False) -> None:
        super().__init__()
        self._path: Path | None = None
        self._worker: _ThumbnailWorker | None = None
        self._interactive = interactive
        self.setObjectName("videoThumbnail")
        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAccessibleName("视频缩略图")
        if interactive:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._show_placeholder()

    def set_video(self, path: Path) -> None:
        resolved = path.resolve()
        self._path = resolved
        self.setToolTip(str(resolved))
        self.setAccessibleName(f"视频缩略图：{resolved.name}")
        self._show_placeholder()
        worker = _ThumbnailWorker(resolved)
        worker.signals.loaded.connect(self._thumbnail_loaded)
        worker.signals.failed.connect(self._thumbnail_failed)
        self._worker = worker
        QThreadPool.globalInstance().start(worker)

    @Slot(Path, object)
    def _thumbnail_loaded(self, path: Path, image: object) -> None:
        if path != self._path or not isinstance(image, QImage) or image.isNull():
            return
        self.setPixmap(self._rounded_pixmap(image))
        self._worker = None

    @Slot(Path)
    def _thumbnail_failed(self, path: Path) -> None:
        if path == self._path:
            self.setAccessibleDescription("视频缩略图暂时无法读取")
            self._worker = None

    def _rounded_pixmap(self, image: QImage) -> QPixmap:
        target = self.size()
        scaled = QPixmap.fromImage(image).scaled(
            target,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        left = max(0, (scaled.width() - target.width()) // 2)
        top = max(0, (scaled.height() - target.height()) // 2)
        cropped = scaled.copy(left, top, target.width(), target.height())

        result = QPixmap(target)
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5, target.width() - 1, target.height() - 1, 10, 10)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped)
        painter.setClipping(False)
        painter.setPen(QPen(QColor("#CFE1BD"), 1))
        painter.drawPath(path)
        painter.end()
        return result

    def _show_placeholder(self) -> None:
        target = self.size()
        pixmap = QPixmap(target)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5, target.width() - 1, target.height() - 1, 10, 10)
        painter.fillPath(path, QColor("#EAF4E0"))
        painter.setPen(QPen(QColor("#D5E8C3"), 1))
        painter.drawPath(path)
        radius = min(target.width(), target.height()) * 0.18
        center_x = target.width() / 2
        center_y = target.height() / 2
        painter.setBrush(QColor("#7DB83B"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        triangle = QPolygonF(
            [
                QPointF(center_x - radius * 0.25, center_y - radius * 0.48),
                QPointF(center_x - radius * 0.25, center_y + radius * 0.48),
                QPointF(center_x + radius * 0.55, center_y),
            ]
        )
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawPolygon(triangle)
        painter.end()
        self.setPixmap(pixmap)

    def mouseReleaseEvent(self, event) -> None:
        if (
            self._interactive
            and event.button() == Qt.MouseButton.LeftButton
            and self.rect().contains(event.position().toPoint())
        ):
            self.activated.emit()
            event.accept()
            return
        super().mouseReleaseEvent(event)


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
    select_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dropArea")
        self.setProperty("active", False)
        self.setProperty("hovered", False)
        self.setProperty("pressed", False)
        self.setProperty("selected", False)
        self.setAcceptDrops(True)
        self.setMinimumHeight(124)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAccessibleName("选择输入视频")
        self.setAccessibleDescription("点击、按回车键，或把视频拖放到这里")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(18, 14, 18, 14)
        self.layout.setSpacing(16)

        self.thumbnail = VideoThumbnail(152, 86)
        self.thumbnail.setVisible(False)
        self.layout.addWidget(self.thumbnail)

        self.copy_layout = QVBoxLayout()
        self.copy_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copy_layout.setSpacing(7)

        self.state_label = QLabel("选择输入视频")
        self.state_label.setObjectName("dropEyebrow")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel("点击选择视频，或直接拖到这里")
        self.title_label.setObjectName("dropTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label = QLabel("支持 MP4、MOV、M4V、AVI、MKV 和 WebM")
        self.hint_label.setObjectName("secondary")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copy_layout.addWidget(self.state_label)
        self.copy_layout.addWidget(self.title_label)
        self.copy_layout.addWidget(self.hint_label)
        self.layout.addLayout(self.copy_layout, 1)

    def set_selected(self, path: Path, width: int, height: int, duration: float) -> None:
        self.setProperty("selected", True)
        self.thumbnail.setVisible(True)
        self.thumbnail.set_video(path)
        self.copy_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        for label in (self.state_label, self.title_label, self.hint_label):
            label.setAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
        self.state_label.setText("✓ 已选择视频")
        self.title_label.setText(path.name)
        self.hint_label.setText(
            f"{width}×{height}  ·  {duration:.1f} 秒  ·  点击或拖入可替换"
        )
        self.setToolTip(str(path))
        self.setAccessibleName(f"已选择视频：{path.name}，点击可替换")
        self._refresh_style()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
            self.setProperty("pressed", True)
            self._refresh_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        was_pressed = bool(self.property("pressed"))
        self.setProperty("pressed", False)
        self._refresh_style()
        if (
            was_pressed
            and self.isEnabled()
            and event.button() == Qt.MouseButton.LeftButton
            and self.rect().contains(event.position().toPoint())
        ):
            self.select_requested.emit()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.select_requested.emit()
            event.accept()
            return
        super().keyPressEvent(event)

    def enterEvent(self, event) -> None:
        self.setProperty("hovered", True)
        self._refresh_style()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setProperty("hovered", False)
        self.setProperty("pressed", False)
        self._refresh_style()
        super().leaveEvent(event)

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
        row.setContentsMargins(10, 9, 10, 9)
        row.setSpacing(12)

        thumbnail = VideoThumbnail(112, 64, interactive=True)
        thumbnail.set_video(path)
        thumbnail.setAccessibleDescription("点击播放视频")
        thumbnail.activated.connect(self.open_video)
        row.addWidget(thumbnail)

        text = QVBoxLayout()
        text.setSpacing(3)
        name = QLabel(path.name)
        name.setObjectName("resultTitle")
        name.setToolTip(path.name)
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
        self.scroll.setMaximumHeight(246)
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
