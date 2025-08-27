#!/bin/bash

source .venv/Scripts/activate
docker-compose up -d
alembic upgrade head


uvicorn app.main:app --reload



