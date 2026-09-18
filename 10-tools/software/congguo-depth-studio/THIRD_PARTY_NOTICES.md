# Third-party components and release review

The application source and Congguo brand assets are internal proprietary assets. A packaged release contains third-party components. The release owner must regenerate and review the complete license manifest from the actual artifact before external distribution.

| Component | Purpose | Review note |
|---|---|---|
| Depth Anything V2 Small | Relative depth | Official Small model is stated as Apache-2.0; Base/Large/Giant differ and are not drop-in replacements |
| ONNX Runtime | CPU inference | Verify the license for the locked version |
| PySide6 / Qt | Desktop UI | Review the applicable LGPL/GPL/commercial distribution obligations |
| OpenCV | Decode and image processing | Verify the license for the locked version |
| imageio-ffmpeg / FFmpeg | Normalize and encode H.264/AAC | Audit the actual FFmpeg build; enabled codecs can affect LGPL/GPL obligations |
| NumPy | Tensor preprocessing | Verify the license for the locked version |

Model upstream: <https://github.com/DepthAnything/Depth-Anything-V2>

Pinned ONNX conversion mirror: <https://huggingface.co/CyberTimon/RapidRAW-Models/blob/daec18e762798acb835d3cda7542d9ecee0dc16b/depth_anything_v2_vits.onnx>

The mirror is not the official upstream. Releases accept it only after matching the SHA-256 recorded
in `src/congguo_depth_studio/resources/MODEL.md`.

Paper: <https://arxiv.org/abs/2406.09414>

Before release:

1. Record locked Python package versions.
2. Inventory bundled frameworks, dynamic libraries, and executables.
3. Confirm Qt and FFmpeg distribution obligations and include required notices.
4. Confirm that only the reviewed Small model is bundled.

This is an engineering checklist, not legal advice.
