.PHONY: lint format typecheck check
 
lint:
	ruff check .
 
format:
	ruff format .
	ruff check --fix .
 
typecheck:
	mypy src/
 
check: lint typecheck