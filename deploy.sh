#!/bin/bash

source .venv/Scripts/activate # or .venv/bin/activate on Linux

pip install -r requirements.txt

[ ! -f .env ] && cp .env.example .env

alembic revision --autogenerate -m "Update db"
alembic upgrade head 

docker-compose up -d

uvicorn app.main:app --reload



