@echo off
del /f db.sqlite3
del /f alembic\versions\*.*
poetry run alembic revision --autogenerate -m "create tables"
poetry run alembic upgrade head
