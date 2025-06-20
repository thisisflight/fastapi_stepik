.DEFAULT_GOAL := help

HOST ?= localhost
PORT ?= 9000

run:
	uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

run-prod:
	poetry run gunicorn app.main:app -c gunicorn.conf.py

push:
	git push -u origin HEAD

lint:
	pre-commit run --all-files

celery:
	celery -A app.backend.celery worker --loglevel=info

help:
	@echo "run - run server (9000 port)"
	@echo "run-prod - run production server"
	@echo "push - push to remote (sets upstream by default)"
	@echo "lint - pre-commit lint"
	@echo "celery - celery worker run"
