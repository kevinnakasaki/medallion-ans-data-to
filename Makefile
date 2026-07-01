.PHONY: setup build up down logs shell run-flow clean init

up:
	docker compose up -d
down:
	docker compose down
build:
	docker compose build worker
logs:
	docker compose logs -f
shell:
	docker compose exec worker bash
run-flow:
	docker compose exec worker python -m src.pipelines.medallion_pipeline
setup: .env
	docker compose run --rm minio-mc
clean:
	docker compose down --volumes
	rm -rf data/
init:
	make setup && make build && make up

.env:
	cp .env.example .env
	@echo "Edit .env with your DATA_URL then run: make setup && make build && make up"

.DEFAULT_GOAL := help
help:
	@echo "Available commands:"
	@echo "  make setup      - Set up the environment"
	@echo "  make build      - Build the Docker images"
	@echo "  make up         - Start the services"
	@echo "  make down       - Stop the services"
	@echo "  make logs       - View logs"
	@echo "  make shell      - Enter the worker shell"
	@echo "  make run-flow   - Run the medallion pipeline"
	@echo "  make clean      - Clean up volumes and data"
	@echo "  make init       - Run setup, build and up in sequence"
	@echo "  make help       - Show this help message"
