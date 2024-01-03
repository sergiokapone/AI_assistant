@echo off
::poetry run python src/main.py
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
