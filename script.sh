#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "[1/6] Detecting Python..."
if command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
else
  echo "Error: Python not found in PATH."
  exit 1
fi

echo "[2/6] Creating virtual environment (.venv)..."
"$PYTHON_CMD" -m venv .venv

echo "[3/6] Activating virtual environment..."
if [ -f ".venv/Scripts/activate" ]; then
  # Windows Git Bash
  # shellcheck disable=SC1091
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  # Linux/macOS
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "Error: activate script not found in .venv"
  exit 1
fi

echo "[4/6] Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[5/6] Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "[6/6] Starting Django development server..."
echo "Server URL: http://127.0.0.1:8000/diagnosis/"
exec python manage.py runserver
