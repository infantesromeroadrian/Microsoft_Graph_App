.PHONY: help install update run dev test clean lint format fix shell build env-check docker-build docker-run docker-stop docker-logs docker-clean docker-prod-build docker-prod-run

# Variables
PYTHON := python
POETRY := poetry
PROJECT_NAME := microsoft-graph-webhook

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

## help: Show this help message
help:
	@echo "$(GREEN)Microsoft Graph Webhook Receiver - Makefile Commands$(NC)"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "$(YELLOW)Setup Commands:$(NC)"
	@echo "  install     - Install project dependencies with Poetry"
	@echo "  update      - Update dependencies to latest versions"
	@echo "  env-check   - Check if .env file exists and show instructions"
	@echo ""
	@echo "$(YELLOW)Development Commands:$(NC)"
	@echo "  run         - Run the webhook server"
	@echo "  dev         - Run the server in development mode with auto-reload"
	@echo "  shell       - Open a Poetry shell"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black (if installed)"
	@echo "  fix         - Fix code issues with ruff"
	@echo ""
	@echo "$(YELLOW)Utility Commands:$(NC)"
	@echo "  clean       - Remove cache files and directories"
	@echo "  build       - Build the project package"
	@echo "  lock        - Update poetry.lock file"
	@echo ""
	@echo "$(YELLOW)Docker Commands:$(NC)"
	@echo "  docker-build      - Build Docker image"
	@echo "  docker-run        - Run container with docker-compose"
	@echo "  docker-stop       - Stop running containers"
	@echo "  docker-logs       - View container logs"
	@echo "  docker-clean      - Remove containers and images"
	@echo "  docker-prod-build - Build production Docker image"
	@echo "  docker-prod-run   - Run production container"

## install: Install project dependencies
install:
	@echo "$(GREEN)Installing dependencies with Poetry...$(NC)"
	$(POETRY) install
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"
	@make env-check

## update: Update dependencies
update:
	@echo "$(GREEN)Updating dependencies...$(NC)"
	$(POETRY) update
	@echo "$(GREEN)Dependencies updated successfully!$(NC)"

## run: Run the webhook server
run: env-check
	@echo "$(GREEN)Starting Microsoft Graph Webhook Server...$(NC)"
	@if [ -n "$$DOCKER_CONTAINER" ] || [ -f /.dockerenv ]; then \
		echo "Running in Docker container..."; \
		$(PYTHON) run.py; \
	else \
		$(POETRY) run python run.py; \
	fi

## dev: Run server in development mode with auto-reload
dev: env-check
	@echo "$(GREEN)Starting server in development mode...$(NC)"
	$(POETRY) run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

## test: Run tests
test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(POETRY) run pytest

## clean: Remove cache files
clean:
	@echo "$(YELLOW)Cleaning cache files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cache cleaned!$(NC)"

## lint: Run linting checks
lint:
	@echo "$(GREEN)Running linting checks...$(NC)"
	$(POETRY) run python -m pylint src/ --errors-only 2>/dev/null || echo "$(YELLOW)Pylint not installed. Install with: poetry add --group dev pylint$(NC)"
	$(POETRY) run python -m mypy src/ 2>/dev/null || echo "$(YELLOW)Mypy not installed. Install with: poetry add --group dev mypy$(NC)"

## format: Format code
format:
	@echo "$(GREEN)Formatting code...$(NC)"
	$(POETRY) run black src/ 2>/dev/null || echo "$(YELLOW)Black not installed. Install with: poetry add --group dev black$(NC)"
	$(POETRY) run isort src/ 2>/dev/null || echo "$(YELLOW)Isort not installed. Install with: poetry add --group dev isort$(NC)"

## fix: Fix code issues with ruff
fix:
	@echo "$(GREEN)Fixing code issues with ruff...$(NC)"
	$(POETRY) run ruff check --fix src/ 2>/dev/null || echo "$(YELLOW)Ruff not installed. Install with: poetry add --group dev ruff$(NC)"
	$(POETRY) run ruff format src/ 2>/dev/null || echo "$(YELLOW)Ruff not installed. Install with: poetry add --group dev ruff$(NC)"
	@echo "$(GREEN)Code fixed!$(NC)"

## shell: Open Poetry shell
shell:
	@echo "$(GREEN)Opening Poetry shell...$(NC)"
	$(POETRY) shell

## build: Build the project
build:
	@echo "$(GREEN)Building project...$(NC)"
	$(POETRY) build

## lock: Update poetry.lock file
lock:
	@echo "$(GREEN)Updating poetry.lock file...$(NC)"
	$(POETRY) lock

## env-check: Check if .env file exists
env-check:
	@if [ -n "$$DOCKER_CONTAINER" ] || [ -f /.dockerenv ]; then \
		echo "$(GREEN)Running in Docker container$(NC)"; \
	elif [ ! -f .env ]; then \
		echo "$(RED)Warning: .env file not found!$(NC)"; \
		echo "$(YELLOW)Please create .env file from env.example:$(NC)"; \
		echo "  cp env.example .env"; \
		echo "  Then edit .env with your Microsoft Graph credentials"; \
		echo ""; \
	else \
		echo "$(GREEN)✓ .env file found$(NC)"; \
	fi

# Docker commands
## docker-build: Build Docker image
docker-build:
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)Docker image built successfully!$(NC)"

## docker-run: Run container with docker-compose
docker-run: env-check
	@echo "$(GREEN)Starting container with docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Container started! Access the API at http://localhost:8000$(NC)"
	@echo "$(YELLOW)View logs with: make docker-logs$(NC)"

## docker-stop: Stop running containers
docker-stop:
	@echo "$(YELLOW)Stopping containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)Containers stopped!$(NC)"

## docker-logs: View container logs
docker-logs:
	docker-compose logs -f

## docker-clean: Remove containers and images
docker-clean:
	@echo "$(RED)Removing containers and images...$(NC)"
	docker-compose down -v
	docker rmi $(PROJECT_NAME):latest || true
	docker rmi $(PROJECT_NAME):prod || true
	@echo "$(GREEN)Docker cleanup complete!$(NC)"

## docker-prod-build: Build production Docker image
docker-prod-build:
	@echo "$(GREEN)Building production Docker image...$(NC)"
	docker build -f Dockerfile.prod -t $(PROJECT_NAME):prod .
	@echo "$(GREEN)Production image built successfully!$(NC)"

## docker-prod-run: Run production container
docker-prod-run:
	@echo "$(GREEN)Starting production container...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)Production container started!$(NC)"

# Quick shortcuts
i: install
r: run
d: dev
t: test
c: clean
f: fix
db: docker-build
dr: docker-run
ds: docker-stop
dl: docker-logs
