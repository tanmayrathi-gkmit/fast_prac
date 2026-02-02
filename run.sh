#!/bin/bash
echo "Starting Database..."
docker-compose up -d

echo "Running Migrations..."
uv run alembic upgrade head

echo "Starting Server..."
uv run uvicorn app.main:app --reload
