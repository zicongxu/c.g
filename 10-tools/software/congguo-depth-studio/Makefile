.PHONY: install download-model install-model run test lint smoke build-macos clean

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade 'pip>=23,<27'
	.venv/bin/pip install -e '.[dev,build]'

download-model:
	./scripts/download-model.sh

install-model:
	@test -n "$(MODEL)" || (echo "Usage: make install-model MODEL=/path/to/depth_anything_v2_vits.onnx"; exit 1)
	./scripts/install-model.sh "$(MODEL)"

run:
	.venv/bin/python -m congguo_depth_studio

test:
	QT_QPA_PLATFORM=minimal .venv/bin/pytest -q

lint:
	.venv/bin/ruff check src tests

smoke:
	QT_QPA_PLATFORM=minimal DEPTH_STUDIO_SMOKE_TEST=1 .venv/bin/python -m congguo_depth_studio

build-macos:
	./scripts/build-macos.sh

clean:
	rm -rf build dist .pytest_cache .ruff_cache
