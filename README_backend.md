docker-compose down -v
docker-compose up -d --build
cd backend
uv run alembic revision --autogenerate -m "create_tables"
# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Start server
uv run uvicorn app.main:app --reload

# Run tests
uv run python test_api.py
