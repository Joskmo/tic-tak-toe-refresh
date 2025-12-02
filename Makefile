.PHONY: help dev prod stop clean logs

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev: ## Start development environment
	docker-compose up --build

dev-d: ## Start development environment in background
	docker-compose up -d --build

prod: ## Start production environment with Traefik
	@if [ ! -f .env.prod ]; then \
		echo "Error: .env.prod not found. Copy env.prod.example and configure it."; \
		exit 1; \
	fi
	@if [ ! -f traefik/acme.json ]; then \
		touch traefik/acme.json && chmod 600 traefik/acme.json; \
	fi
	docker network create web 2>/dev/null || true
	docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

stop: ## Stop all containers
	docker-compose down
	docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

clean: ## Stop and remove all containers, volumes, and networks
	docker-compose down -v
	docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true

logs: ## Show logs from all containers
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-traefik: ## Show Traefik logs
	docker-compose -f docker-compose.prod.yml logs -f traefik

backend-shell: ## Open shell in backend container
	docker-compose exec backend sh

frontend-shell: ## Open shell in frontend container
	docker-compose exec frontend sh

install-backend: ## Install backend dependencies locally
	cd backend && uv sync

install-frontend: ## Install frontend dependencies locally
	cd frontend && npm install

test-backend: ## Run backend tests
	cd backend && uv run pytest

build: ## Build all images
	docker-compose build

prod-build: ## Build production images
	docker-compose -f docker-compose.prod.yml build

