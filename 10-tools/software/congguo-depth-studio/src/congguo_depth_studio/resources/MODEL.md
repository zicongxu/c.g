# Model contract

| Field | Value |
|---|---|
| File | `depth_anything_v2_vits.onnx` |
| Family | Depth Anything V2 Small (ViT-S) |
| Task | Monocular relative-depth estimation |
| Input | RGB float32, `1x3x518x518`, ImageNet mean/std |
| Output | Single-channel float32 relative depth |
| Accepted size | approximately 95 MiB |
| SHA-256 | `d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be` |
| Upstream license | Apache-2.0 for Depth Anything V2 Small |
| Git policy | excluded; download and verify during setup |

## Sources and provenance

- Official model family, source, checkpoint, and license:
  <https://github.com/DepthAnything/Depth-Anything-V2>
- Pinned public ONNX artifact used by this application:
  <https://huggingface.co/CyberTimon/RapidRAW-Models/blob/daec18e762798acb835d3cda7542d9ecee0dc16b/depth_anything_v2_vits.onnx>

The official project publishes the Small checkpoint as PyTorch weights, not this exact ONNX file.
The ONNX URL is therefore a third-party conversion mirror, pinned to a repository revision rather
than `main`. Its downloaded bytes and the model embedded in the current App were independently
verified on 2026-09-19 to match the SHA-256 above. Hash validation is mandatory because the mirror
is not controlled by Congguo or the official model authors.

Install to:

```text
src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx
```

Download and verify the pinned public artifact:

```bash
make download-model
```

For an offline or internally mirrored artifact, use the verified local installer instead:

```bash
./scripts/install-model.sh /absolute/path/depth_anything_v2_vits.onnx
```

`DEPTH_STUDIO_MODEL_URL` may point `download-model.sh` at a company-controlled mirror, but the
download must retain the same accepted SHA-256.

## Replacing the model

1. Confirm commercial-use licensing; upstream Small and Base/Large/Giant licenses differ.
2. Update input size, normalization, channel order, and output parsing as required.
3. Update this file and the URL/checksums in download, install, and build scripts.
4. Compare polarity, flicker, edges, speed, and memory on a fixed sanitized regression clip.
5. Repeat packaged end-to-end and third-party license acceptance.
