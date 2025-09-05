"""
Router for handling Microsoft Graph webhook notifications
"""

import json
import logging

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse

from src.schemas.notifications import ChangeNotificationCollection
from src.services.mail_notification_service import MailNotificationService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    responses={404: {"description": "Not found"}},
)

# Initialize mail notification service
mail_notification_service = MailNotificationService()


@router.post("")
async def receive_notification(request: Request, validationToken: str | None = None):
    """
    Endpoint to receive notifications from Microsoft Graph

    This endpoint handles:
    1. Subscription validation (when validationToken is present)
    2. Change notifications (when notification data is present)
    """

    # Handle subscription validation
    if validationToken:
        logger.info(f"Validating subscription with token: {validationToken}")
        return PlainTextResponse(content=validationToken)

    # Handle change notifications
    try:
        body = await request.body()
        data = json.loads(body)

        logger.info(f"Received notification: {json.dumps(data, indent=2)}")

        # Parse the notification collection
        notification_collection = ChangeNotificationCollection(**data)

        # Process each notification
        for notification in notification_collection.value:
            await mail_notification_service.process_mail_notification(notification)

        # Return 202 Accepted
        return Response(status_code=202)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Error processing notification: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Microsoft Graph Webhook Receiver",
        "graph_configured": bool(mail_notification_service.graph_service.access_token),
    }
