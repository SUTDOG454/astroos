.PHONY: test up down logs

test:
	python -m pytest -q

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f ingestion sink
