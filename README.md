# Microsoft Graph Webhook Receiver

A FastAPI-based webhook receiver for Microsoft Graph mail notifications with a clean, modular architecture.

## 🚀 Features

- Receives real-time mail notifications from Microsoft Graph
- Fetches full mail details including subject, sender, and body preview
- Clean modular architecture with services, routers, and schemas
- Configuration management with environment variables
- Comprehensive logging
- Health check endpoint

## 📁 Project Structure

```
Microsoft_graph_app/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── main.py            # FastAPI application
│   ├── routers/
│   │   ├── __init__.py
│   │   └── notifications.py # Webhook endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── notifications.py # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── graph_service.py # Microsoft Graph API logic
├── .env.example           # Example environment variables
├── .gitignore
├── requirements.txt       # Python dependencies
└── run.py                # Entry point script
```

## 🛠️ Setup

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management) - [Install Poetry](https://python-poetry.org/docs/#installation)
- Make (optional, for easier command execution)

### 1. Clone the repository

```bash
git clone <repository-url>
cd Microsoft_graph_app
```

### 2. Install dependencies

#### Using Make (recommended):

```bash
make install
```

#### Using Poetry directly:

```bash
poetry install
```

#### Using pip (alternative):

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp env.example .env
```

Edit `.env` with your Microsoft Graph credentials:

```env
# Microsoft Graph Configuration
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
ACCESS_TOKEN=your-access-token

# Server Configuration (optional)
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Logging Configuration (optional)
LOG_LEVEL=INFO

# Payment Notification Configuration (optional)
PAYMENT_NOTIFICATION_RECIPIENT=admin@yourcompany.com
```

## 🚀 Running the Application

### Using Make (recommended):

```bash
# Run in production mode
make run

# Run in development mode with auto-reload
make dev
```

### Using Poetry:

```bash
# Run the server
poetry run python run.py

# Or run in development mode
poetry run uvicorn src.main:app --reload
```

### Using Python directly:

```bash
python run.py
```

The application will start on `http://localhost:8000`

## 📋 Available Make Commands

```bash
make help       # Show all available commands
make install    # Install dependencies
make update     # Update dependencies
make run        # Run the server
make dev        # Run in development mode
make test       # Run tests
make lint       # Run linting checks
make format     # Format code
make clean      # Clean cache files
make shell      # Open Poetry shell
```

## 📍 Endpoints

- `GET /` - Root endpoint with basic info
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)
- `POST /api/notifications` - Webhook endpoint for Microsoft Graph
- `GET /api/notifications/health` - Health check endpoint

## 🔧 Development

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Logging

The application uses Python's built-in logging. Configure the log level using the `LOG_LEVEL` environment variable.

### Testing the webhook

You can test the webhook endpoint using curl:

```bash
# Test validation
curl -X POST http://localhost:8000/api/notifications?validationToken=test123

# Test notification (example)
curl -X POST http://localhost:8000/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "value": [{
      "changeType": "created",
      "resource": "Users/user-id/Messages/message-id",
      "subscriptionId": "subscription-id",
      "tenantId": "tenant-id"
    }]
  }'
```

## 📝 License

[Your License Here]

## 👥 Contributing

[Your Contributing Guidelines Here]