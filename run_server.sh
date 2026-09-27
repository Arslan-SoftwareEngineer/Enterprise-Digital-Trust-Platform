#!/usr/bin/env bash
# Quick launch script for Enterprise Digital Identity, Trust & Deepfake Detection Platform
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "================================================================="
echo "Enterprise Digital Identity, Trust & Deepfake Detection Platform"
echo "================================================================="

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

export PYTHONPATH="."
echo "Starting FastAPI Application Gateway on http://localhost:8000 ..."
exec ./venv/bin/python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
