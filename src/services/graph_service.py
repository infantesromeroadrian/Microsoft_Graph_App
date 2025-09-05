"""
Service for interacting with Microsoft Graph API
"""

import logging
from typing import Any

import httpx

from src.config import settings
from src.schemas.notifications import MailDetails

logger = logging.getLogger(__name__)


class GraphService:
    """Service to handle Microsoft Graph API operations"""

    def __init__(self):
        self.graph_api_url = settings.graph_api_url
        self.access_token = settings.access_token

    async def send_mail(self, subject: str, message: str, recipient: str) -> bool:
        """Send an email using Microsoft Graph API

        Args:
            subject: Email subject
            message: Email body content
            recipient: Recipient email address

        Returns:
            True if email was sent successfully, None otherwise
        """
        if not self.access_token:
            logger.error("No access token configured")
            return None
        url = f"{self.graph_api_url}/me/sendmail"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        data = {
            "message": {
                "subject": subject,
                "body": {"contentType": "Text", "content": message},
                "toRecipients": [{"emailAddress": {"address": recipient}}],
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            # 202 is accepted for async send mail operation
            if response.status_code in [200, 202]:
                logger.info("Email sent successfully")
                return True
            else:
                logger.error(
                    f"Failed to send mail: {response.status_code} - {response.text}"
                )
                return None

    async def get_mail_details(
        self, user_id: str, message_id: str
    ) -> MailDetails | None:
        """
        Fetch full mail details from Microsoft Graph

        Args:
            user_id: The user ID
            message_id: The message ID

        Returns:
            MailDetails object or None if failed
        """
        if not self.access_token:
            logger.error("No access token configured")
            return None

        url = f"{self.graph_api_url}/users/{user_id}/messages/{message_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30.0)

                if response.status_code == 200:
                    data = response.json()
                    return self._parse_mail_details(data)
                else:
                    logger.error(
                        f"Failed to get mail details: "
                        f"{response.status_code} - {response.text}"
                    )
                    return None

        except Exception as e:
            logger.error(f"Error fetching mail details: {e}")
            return None

    def _parse_mail_details(self, data: dict[str, Any]) -> MailDetails:
        """Parse raw mail data into MailDetails object"""
        from_email = data.get("from", {}).get("emailAddress", {})

        # Extract body preview
        body_content = data.get("body", {})
        body_preview = data.get("bodyPreview", "")

        if not body_preview and body_content.get("contentType") == "text":
            body_preview = body_content.get("content", "")[:500]  # Limit to 500 chars

        return MailDetails(
            id=data.get("id", ""),
            subject=data.get("subject", "Sin asunto"),
            from_name=from_email.get("name", "Sin nombre"),
            from_address=from_email.get("address", "Desconocido"),
            body_preview=body_preview or "Sin contenido",
            received_datetime=data.get("receivedDateTime"),
            has_attachments=data.get("hasAttachments", False),
            importance=data.get("importance", "normal"),
        )

    @staticmethod
    def extract_user_and_message_id(
        resource: str,
    ) -> tuple[str | None, str | None]:
        """
        Extract user ID and message ID from resource path

        Args:
            resource: Resource path like 'Users/{user-id}/Messages/{message-id}'

        Returns:
            Tuple of (user_id, message_id)
        """
        parts = resource.split("/")
        user_id = None
        message_id = None

        for i, part in enumerate(parts):
            if part.lower() == "users" and i + 1 < len(parts):
                user_id = parts[i + 1]
            elif part.lower() == "messages" and i + 1 < len(parts):
                message_id = parts[i + 1]

        return user_id, message_id
