set shell := ["powershell.exe", "-c"]

lint:
    uv run ec ./src
    uv run ruff check ./src
    uv run --with pydantic mypy ./src

format:
    uv ruff check --fix ./src

test:
    uv run pytest -vv
