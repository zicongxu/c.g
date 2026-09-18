.PHONY: install test lint smoke clean

DEPTH_STUDIO := ../../software/congguo-depth-studio

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade 'pip>=23,<27'
	.venv/bin/pip install -e '$(DEPTH_STUDIO)'
	.venv/bin/pip install -e '.[dev]'

test:
	.venv/bin/pytest -q

lint:
	.venv/bin/ruff check src tests

smoke:
	PYTHONPATH=src .venv/bin/python -m cgcli --help >/dev/null
	PYTHONPATH=src .venv/bin/python -m cgcli video depth --help >/dev/null

clean:
	rm -rf .pytest_cache .ruff_cache build dist
