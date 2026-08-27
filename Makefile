.PHONY: live paper test lint

live:
	python scripts/live.py --config config/default.yaml

paper:
	python scripts/paper.py --config config/default.yaml

test:
	pytest tests/ -v --tb=short

lint:
	ruff check src/ && mypy src/
