---
title: Congguo Depth Studio Operations Guide
summary: Runtime data, storage, performance, troubleshooting, and safe incident collection
status: draft
owner: Congguo Product Team
updated: 2026-09-18
review_cycle: event-driven
source_of_truth: true
confidentiality: internal
tags: [operations, troubleshooting, desktop-app]
related: [../README.md, architecture.md, build-and-release.md]
---

# Operations guide

## Runtime behavior

- Inference is CPU-based and processing time grows approximately with frame count.
- Output dimensions match the source; model inference stays fixed at `518x518`.
- Preprocessing converts the source to the selected constant frame rate.
- Temporary storage contains normalized input, silent depth video, and final encode. Keep at least three times the input file size free.

## Data locations

- Input: user-selected source, read-only.
- Output: `<source-stem>_depth.mp4` beside the source unless the user chooses another path.
- Intermediate files: `depth-motion-*` under the system temporary directory.
- Recent outputs: `recentOutputs` in Qt `QSettings`, at most eight local paths.
- Packaged model: `resources/depth_anything_v2_vits.onnx` inside the app bundle.

## Troubleshooting

### macOS blocks first launch

The internal build is ad-hoc signed and not notarized. Control-click the app in Finder and select Open. External distribution must use Developer ID signing and notarization instead of relying on this workaround.

### Built-in model is missing

For source runs, execute `install-model.sh` and confirm the target path. For a packaged app, the build omitted the model: inspect the spec `datas` list and rebuild. Never fix this by committing the model to Git.

### Video cannot be read

Confirm the extension is supported and use `ffprobe` or VLC to verify the file. If FFmpeg decodes it but OpenCV probing does not, record the codec/container and consider replacing the probe with FFprobe; do not merely widen the extension list.

### Final encoding fails

Confirm destination permissions and free disk space, and verify the imageio-ffmpeg binary is bundled. The user dialog includes the final 800 characters of FFmpeg stderr.

### Layout is clipped or overlapping

Confirm version 2.1.0 or later, the central `QScrollArea`, the 132-pixel header, and the 112-pixel mascot. Reproduce at `680x600` and the user's display scale, not only on a large monitor.

### Processing is slow or CPU use is high

CPU inference is compute-heavy. ONNX intra-op threads are limited to `min(8, CPU count)`. Prefer 24/30 FPS unless 60 FPS is a real requirement. High source resolution still increases resize and encoding work even though inference is `518x518`.

## Safe incident collection

Collect app version, OS, CPU architecture, free disk, and sanitized media metadata (container, codec, dimensions, FPS, duration, audio presence). Record the failed stage and dialog text. Ask for a minimal non-sensitive reproduction clip, not a personal source video.
