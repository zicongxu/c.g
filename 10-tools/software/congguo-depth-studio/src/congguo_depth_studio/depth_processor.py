from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
import onnxruntime as ort

from .contracts import CancelCallback, ProcessingCancelled, ProgressCallback

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def probe_video(path: str | Path) -> dict[str, float | int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("无法读取这个视频文件")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    cap.release()
    duration = frames / fps if fps > 0 else 0
    return {"width": width, "height": height, "fps": fps, "duration": duration}


class DepthProcessor:
    def __init__(self, model_path: Path, progress: ProgressCallback, cancelled: CancelCallback):
        self.model_path = model_path
        self.progress = progress
        self.cancelled = cancelled
        self.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    def run(self, input_path: Path, output_path: Path, fps: int, keep_audio: bool) -> None:
        if not input_path.exists():
            raise FileNotFoundError("输入视频不存在")
        if not self.model_path.exists():
            raise FileNotFoundError("应用内置的深度模型缺失")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.progress(1, "正在准备视频…", None)

        with tempfile.TemporaryDirectory(prefix="depth-motion-") as temp_dir:
            temp = Path(temp_dir)
            cfr_path = temp / "input_cfr.mp4"
            silent_path = temp / "depth_silent.mp4"
            final_path = temp / "final.mp4"

            self._make_constant_fps(input_path, cfr_path, fps)
            self._check_cancelled()
            self.progress(7, "正在加载深度模型…", None)
            self._infer_video(cfr_path, silent_path, fps)
            self._check_cancelled()
            self.progress(94, "正在编码最终视频…", None)
            self._encode_final(silent_path, input_path, final_path, keep_audio)
            self._check_cancelled()
            shutil.move(str(final_path), str(output_path))
            self.progress(100, "处理完成", 0)

    def _make_constant_fps(self, source: Path, target: Path, fps: int) -> None:
        command = [
            self.ffmpeg, "-y", "-loglevel", "error", "-i", str(source),
            "-map", "0:v:0", "-vf", f"fps={fps}", "-an",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "10",
            "-pix_fmt", "yuv420p", str(target),
        ]
        self._run_process(command, "视频预处理失败")

    def _create_session(self) -> ort.InferenceSession:
        options = ort.SessionOptions()
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        options.intra_op_num_threads = min(8, os.cpu_count() or 4)
        return ort.InferenceSession(
            str(self.model_path), sess_options=options, providers=["CPUExecutionProvider"]
        )

    def _infer_video(self, source: Path, target: Path, fps: int) -> None:
        cap = cv2.VideoCapture(str(source))
        if not cap.isOpened():
            raise RuntimeError("无法打开预处理后的视频")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total = max(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        writer = cv2.VideoWriter(
            str(target), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height), True
        )
        if not writer.isOpened():
            cap.release()
            raise RuntimeError("无法创建深度视频")

        try:
            session = self._create_session()
            input_name = session.get_inputs()[0].name
            ema_low: float | None = None
            ema_high: float | None = None
            started = time.monotonic()
            index = 0

            while True:
                self._check_cancelled()
                ok, frame = cap.read()
                if not ok:
                    break

                tensor = self._preprocess(frame)
                raw = session.run(None, {input_name: tensor})[0]
                depth = np.squeeze(raw).astype(np.float32)
                depth = cv2.resize(depth, (width, height), interpolation=cv2.INTER_CUBIC)
                low, high = np.percentile(depth, (1.0, 99.0))
                if ema_low is None:
                    ema_low, ema_high = float(low), float(high)
                else:
                    ema_low = 0.88 * ema_low + 0.12 * float(low)
                    ema_high = 0.88 * ema_high + 0.12 * float(high)

                normalized = np.clip(
                    (depth - ema_low) / max(ema_high - ema_low, 1e-6), 0.0, 1.0
                )
                gray = np.uint8(np.round(np.power(normalized, 0.82) * 255.0))
                gray = cv2.bilateralFilter(gray, 5, 18, 5)
                writer.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

                index += 1
                if index == 1 or index % 3 == 0 or index == total:
                    elapsed = time.monotonic() - started
                    rate = index / max(elapsed, 1e-6)
                    eta = max(0.0, (total - index) / max(rate, 1e-6))
                    percent = 8 + int(84 * index / total)
                    self.progress(percent, f"正在提取深度 · {index}/{total} 帧", eta)
        finally:
            cap.release()
            writer.release()

    @staticmethod
    def _preprocess(frame: np.ndarray) -> np.ndarray:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (518, 518), interpolation=cv2.INTER_CUBIC)
        rgb = rgb.astype(np.float32) / 255.0
        rgb = (rgb - MEAN) / STD
        return np.ascontiguousarray(rgb.transpose(2, 0, 1)[None], dtype=np.float32)

    def _encode_final(
        self, silent: Path, source: Path, target: Path, keep_audio: bool
    ) -> None:
        command = [self.ffmpeg, "-y", "-loglevel", "error", "-i", str(silent)]
        if keep_audio:
            command += ["-i", str(source), "-map", "0:v:0", "-map", "1:a:0?"]
        command += [
            "-c:v", "libx264", "-preset", "medium", "-crf", "14",
            "-pix_fmt", "yuv420p",
        ]
        if keep_audio:
            command += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
        command += ["-movflags", "+faststart", str(target)]
        self._run_process(command, "最终视频编码失败")

    def _run_process(self, command: list[str], failure_message: str) -> None:
        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True
        )
        while process.poll() is None:
            if self.cancelled():
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                raise ProcessingCancelled("操作已取消")
            time.sleep(0.1)
        stderr = process.stderr.read().strip() if process.stderr else ""
        if process.returncode != 0:
            raise RuntimeError(f"{failure_message}\n{stderr[-800:]}")

    def _check_cancelled(self) -> None:
        if self.cancelled():
            raise ProcessingCancelled("操作已取消")
