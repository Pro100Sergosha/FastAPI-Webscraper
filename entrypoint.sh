#!/bin/sh
set -e

echo "Applying migrations..."
uv run alembic upgrade head

exec "$@"