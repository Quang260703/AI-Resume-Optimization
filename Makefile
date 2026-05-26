.PHONY: lint format typecheck test check

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

typecheck:
	python -m mypy src/

test:
	pytest tests/

check: lint format typecheck test