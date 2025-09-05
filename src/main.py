"""
Main application entry point
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers import notifications

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level), format=settings.log_format
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Webhook receiver for Microsoft Graph mail notifications",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notifications.router, prefix=settings.api_prefix)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Microsoft Graph Webhook Receiver",
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Microsoft Graph Webhook Receiver",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Listening on {settings.host}:{settings.port}")

    # Log configuration status
    if settings.access_token:
        logger.info("✅ Access token configured")
    else:
        logger.warning(
            "⚠️  No access token configured - mail details fetching will not work"
        )
        logger.info("To configure, set ACCESS_TOKEN in your .env file")


def start():
    """Start the application using uvicorn"""
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    start()
