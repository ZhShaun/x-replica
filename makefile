.PHONY: run lint format check

# Run the FastAPI server with uvicorn, assuming your app is in main.py
run:
	@echo "🚀 Starting FastAPI server on http://localhost:8000"
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

format:
	@echo "🎨 Formatting code with Ruff..."
	ruff format .

lint:
	@echo "✅ Linting and fixing with Ruff..."
	ruff check . --fix

type-check:
	@echo "🧐 Running static type checking with Mypy..."
	mypy .

check: format lint type-check
	@echo "✅ All checks passed."

