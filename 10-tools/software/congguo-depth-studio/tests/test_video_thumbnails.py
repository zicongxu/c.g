from __future__ import annotations

from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtTest import QSignalSpy, QTest
from PySide6.QtWidgets import QApplication

from congguo_depth_studio import widgets


class FakeCapture:
    def __init__(self, frame: np.ndarray) -> None:
        self.frame = frame
        self.released = False
        self.frame_positions: list[int] = []

    def isOpened(self) -> bool:
        return True

    def get(self, property_id: int) -> int:
        assert property_id == widgets.cv2.CAP_PROP_FRAME_COUNT
        return 100

    def set(self, property_id: int, value: int) -> bool:
        if property_id == widgets.cv2.CAP_PROP_POS_FRAMES:
            self.frame_positions.append(value)
        return True

    def read(self) -> tuple[bool, np.ndarray]:
        return True, self.frame

    def release(self) -> None:
        self.released = True


def test_thumbnail_extracts_an_rgb_qimage_from_a_representative_frame(monkeypatch) -> None:
    bgr_frame = np.array([[[10, 20, 30], [40, 50, 60]]], dtype=np.uint8)
    capture = FakeCapture(bgr_frame)
    monkeypatch.setattr(widgets.cv2, "VideoCapture", lambda _path: capture)

    image = widgets.extract_video_thumbnail(Path("sample.mp4"))

    assert image.width() == 2
    assert image.height() == 1
    assert capture.frame_positions == [12]
    assert capture.released is True
    assert image.pixelColor(0, 0).getRgb()[:3] == (30, 20, 10)


def test_drop_area_is_a_clickable_and_keyboard_accessible_video_hotspot() -> None:
    app = QApplication.instance() or QApplication([])
    area = widgets.DropArea()
    area.show()
    spy = QSignalSpy(area.select_requested)

    QTest.mouseClick(area, Qt.MouseButton.LeftButton)
    area.setFocus()
    QTest.keyClick(area, Qt.Key.Key_Return)

    assert spy.count() == 2
    area.close()
    app.processEvents()
