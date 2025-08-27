#!/bin/bash

source .venv/Scripts/activate # or .venv/bin/activate on Linux

pip install -r requirements.txt

docker-compose up -d
alembic upgrade head


uvicorn app.main:app --reload



