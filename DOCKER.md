# Docker Setup for Microsoft Graph Webhook Receiver

This guide explains how to build and run the Microsoft Graph Webhook Receiver using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed (usually comes with Docker Desktop)
- `.env` file configured with your Microsoft Graph credentials

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and run the container
make docker-run

# Or using docker-compose directly
docker-compose up -d
```

The application will be available at `http://localhost:8000`

### 2. View Logs

```bash
# View container logs
make docker-logs

# Or using docker-compose
docker-compose logs -f
```

### 3. Stop the Container

```bash
# Stop the container
make docker-stop

# Or using docker-compose
docker-compose down
```

## Production Deployment

### Build Production Image

The production Dockerfile uses a multi-stage build for a smaller, more secure image:

```bash
# Build production image
make docker-prod-build

# Or using docker directly
docker build -f Dockerfile.prod -t microsoft-graph-webhook:prod .
```

### Run Production Container

```bash
# Create .env.prod file with production credentials
cp .env .env.prod
# Edit .env.prod with production values

# Run production container
make docker-prod-run

# Or using docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## Docker Commands Reference

### Using Make (Recommended)

- `make docker-build` - Build Docker image
- `make docker-run` - Run container with docker-compose
- `make docker-stop` - Stop running containers
- `make docker-logs` - View container logs
- `make docker-clean` - Remove containers and images
- `make docker-prod-build` - Build production Docker image
- `make docker-prod-run` - Run production container

**Note**: The Docker containers use `make run` internally to start the application, which automatically detects the Docker environment and runs without Poetry.

### Using Docker Directly

```bash
# Build image
docker build -t microsoft-graph-webhook:latest .

# Run container
docker run -d \
  --name microsoft-graph-webhook \
  -p 8000:8000 \
  --env-file .env \
  microsoft-graph-webhook:latest

# View logs
docker logs -f microsoft-graph-webhook

# Stop container
docker stop microsoft-graph-webhook

# Remove container
docker rm microsoft-graph-webhook
```

## Environment Variables

The Docker container uses the same environment variables as the local development. Create a `.env` file based on `env.example`:

```bash
cp env.example .env
```

Required variables:
- `ACCESS_TOKEN` - Microsoft Graph access token (for fetching mail details)

Optional variables:
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: False)
- `LOG_LEVEL` - Logging level (default: INFO)
- `PAYMENT_NOTIFICATION_RECIPIENT` - Email for payment notifications (default: admin@company.com)

## Docker Compose Configuration

### Development (docker-compose.yml)

- Mounts `.env` file for easy configuration updates
- Includes health checks
- Auto-restart policy: `unless-stopped`
- Exposes port 8000

### Production (docker-compose.prod.yml)

- Uses optimized production image
- Stricter resource limits
- Maps to port 80
- Auto-restart policy: `always`
- Requires `.env.prod` file

## Troubleshooting

### Container won't start

1. Check logs: `docker-compose logs`
2. Verify `.env` file exists and is properly configured
3. Ensure port 8000 (or 80 for production) is not in use

### Can't access the API

1. Verify container is running: `docker ps`
2. Check health status: `docker ps --format "table {{.Names}}\t{{.Status}}"`
3. Test locally: `docker exec microsoft-graph-webhook curl http://localhost:8000/health`

### Environment variables not loading

1. Ensure `.env` file is in the project root
2. Check file permissions
3. Verify variable names match exactly (case-sensitive)

## Security Considerations

1. The production Dockerfile runs as a non-root user for security
2. Only necessary files are copied to the image (via .dockerignore)
3. Multi-stage build reduces final image size and attack surface
4. Health checks ensure container reliability
5. Resource limits prevent container from consuming excessive resources

## Best Practices

1. Always use `.env` files for sensitive configuration
2. Never commit `.env` files to version control
3. Use production Dockerfile for deployments
4. Monitor container logs regularly
5. Set up proper SSL/TLS termination in production (e.g., using a reverse proxy)
