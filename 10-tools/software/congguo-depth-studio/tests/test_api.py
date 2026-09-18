from __future__ import annotations

from congguo_depth_studio import api


def test_extract_depth_video_returns_typed_result(tmp_path, monkeypatch) -> None:
    source = tmp_path / "source.mp4"
    model = tmp_path / "depth.onnx"
    output = tmp_path / "source_depth.mp4"
    source.touch()
    model.touch()
    calls = []

    class FakeProcessor:
        def __init__(self, model_path, progress, cancelled):
            calls.append((model_path, progress, cancelled))

        def run(self, input_path, output_path, fps, keep_audio):
            calls.append((input_path, output_path, fps, keep_audio))

    monkeypatch.setattr(api, "_load_processor_type", lambda: FakeProcessor)
    request = api.DepthRequest(source, output, model, fps=24, keep_audio=False)

    result = api.extract_depth_video(request)

    assert result.input_path == source
    assert result.output_path == output
    assert result.fps == 24
    assert result.keep_audio is False
    assert calls[1] == (source, output, 24, False)


def test_extract_depth_video_refuses_existing_output(tmp_path) -> None:
    source = tmp_path / "source.mp4"
    model = tmp_path / "depth.onnx"
    output = tmp_path / "source_depth.mp4"
    source.touch()
    model.touch()
    output.touch()

    request = api.DepthRequest(source, output, model)

    try:
        api.extract_depth_video(request)
    except api.OutputAlreadyExists as exc:
        assert exc.code == "OUTPUT_ALREADY_EXISTS"
    else:
        raise AssertionError("existing output should be rejected")
