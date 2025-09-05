"""
Service for processing mail notifications from Microsoft Graph
"""

import logging

from src.schemas.notifications import ChangeNotification
from src.services.graph_service import GraphService
from src.services.payment_notification_service import PaymentNotificationService

logger = logging.getLogger(__name__)


class MailNotificationService:
    """Service to handle mail notification processing"""

    def __init__(self):
        self.graph_service = GraphService()
        self.payment_notification_service = PaymentNotificationService()

    async def process_mail_notification(self, notification: ChangeNotification):
        """Process individual mail notification"""
        try:
            # Only process mail messages
            if "messages" not in notification.resource.lower():
                logger.debug(f"Skipping non-mail notification: {notification.resource}")
                return

            logger.info(
                f"Processing mail notification - Type: {notification.changeType}"
            )

            # Extract user ID and message ID
            user_id, message_id = self.graph_service.extract_user_and_message_id(
                notification.resource
            )

            if not user_id or not message_id:
                logger.error(
                    f"Could not extract user/message ID from resource: "
                    f"{notification.resource}"
                )
                return

            logger.info(
                f"Fetching details for message {message_id} from user {user_id}"
            )

            # Fetch mail details
            mail_details = await self.graph_service.get_mail_details(
                user_id, message_id
            )

            if mail_details:
                # Log mail details in a clean format
                logger.info("\n")
                logger.info("=" * 60)
                logger.info("📧 NUEVO CORREO RECIBIDO")
                logger.info("=" * 60)
                logger.info(
                    f"DE: {mail_details.from_name} <{mail_details.from_address}>"
                )
                logger.info(f"ASUNTO: {mail_details.subject}")
                logger.info(f"FECHA: {mail_details.received_datetime}")
                logger.info(f"IMPORTANCIA: {mail_details.importance}")
                logger.info(
                    f"TIENE ADJUNTOS: {'Sí' if mail_details.has_attachments else 'No'}"
                )
                logger.info("-" * 60)
                logger.info("VISTA PREVIA:")
                logger.info(mail_details.body_preview)
                logger.info("=" * 60)
                logger.info("\n")

                # Process payment notification if applicable
                await self.payment_notification_service.process_payment_email(
                    mail_details
                )
            else:
                logger.warning(f"Could not fetch details for message {message_id}")

        except Exception as e:
            logger.error(f"Error processing mail notification: {e}", exc_info=True)
