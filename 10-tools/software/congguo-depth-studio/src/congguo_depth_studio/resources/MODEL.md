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
| Git policy | excluded; install from controlled storage |

Install to:

```text
src/congguo_depth_studio/resources/depth_anything_v2_vits.onnx
```

Use the verified installer:

```bash
./scripts/install-model.sh /absolute/path/depth_anything_v2_vits.onnx
```

## Replacing the model

1. Confirm commercial-use licensing; upstream Small and Base/Large/Giant licenses differ.
2. Update input size, normalization, channel order, and output parsing as required.
3. Update this file and the checksums in both install/build scripts.
4. Compare polarity, flicker, edges, speed, and memory on a fixed sanitized regression clip.
5. Repeat packaged end-to-end and third-party license acceptance.
