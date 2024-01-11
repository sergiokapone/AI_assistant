@echo off
del /f db.sqlite3
del /f alembic\versions\*.*
rmdir /s /q chromadb
rmdir /s /q uploads
poetry run alembic revision --autogenerate -m "create tables"
poetry run alembic upgrade head
