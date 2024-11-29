#!/usr/bin/env bash
set -euo pipefail
echo "Run black"
poetry run black .
echo "Run isort"
poetry run isort .
echo "Run mypy"
poetry run mypy .
echo "Run tests"
python manage.py test
echo "All checks passed!"
