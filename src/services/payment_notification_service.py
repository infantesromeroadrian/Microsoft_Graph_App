"""
Service for handling payment-related email notifications
"""

import logging
import re

from src.config import settings
from src.schemas.notifications import MailDetails
from src.services.graph_service import GraphService

logger = logging.getLogger(__name__)


class PaymentNotificationService:
    """Service to handle payment-related email notifications"""

    def __init__(self):
        self.graph_service = GraphService()
        # Payment-related keywords to check in subject
        self.payment_keywords = [
            r"\bpago\b",
            r"\bpagos\b",
            r"\bpagar\b",
            r"\bpagado\b",
            r"\bpagó\b",
            r"\bpagué\b",
            r"\bpaguè\b",
            r"\bpagamos\b",
            r"\bpagaron\b",
            r"\bpayment\b",
            r"\bpaid\b",
            r"\bpay\b",
        ]
        self.payment_pattern = re.compile(
            "|".join(self.payment_keywords), re.IGNORECASE
        )
        # Default recipient for payment notifications (configurable)
        self.notification_recipient = settings.payment_notification_recipient or "admin@company.com"

    def check_payment_subject(self, subject: str) -> bool:
        """
        Check if the email subject contains payment-related keywords

        Args:
            subject: The email subject to check

        Returns:
            True if payment-related keywords found, False otherwise
        """
        if not subject:
            return False

        # Check if subject matches any payment pattern
        if self.payment_pattern.search(subject):
            logger.info(f"Payment-related email detected! Subject: {subject}")
            return True

        return False

    async def process_payment_email(self, mail_details: MailDetails) -> bool:
        """
        Process payment-related email and send notification if needed

        Args:
            mail_details: The mail details object

        Returns:
            True if notification was sent, False otherwise
        """
        if not self.check_payment_subject(mail_details.subject):
            return False

        await self.send_payment_notification(mail_details)
        return True

    async def send_payment_notification(
        self, mail_details: MailDetails, recipient: str | None = None
    ) -> bool:
        """
        Send notification email about payment-related message

        Args:
            mail_details: The mail details object
            recipient: Optional recipient email (defaults to configured recipient)

        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Use provided recipient or default
            recipient_email = recipient or self.notification_recipient

            # Prepare notification email
            subject = f"🔔 Notificación de Pago: {mail_details.subject}"

            message = f"""
Se ha recibido un correo relacionado con pagos:

📧 DETALLES DEL CORREO:
------------------------
De: {mail_details.from_name} <{mail_details.from_address}>
Asunto: {mail_details.subject}
Fecha: {mail_details.received_datetime}
Importancia: {mail_details.importance}
Tiene adjuntos: {"Sí" if mail_details.has_attachments else "No"}

📝 VISTA PREVIA:
------------------------
{mail_details.body_preview}

------------------------
Este es un mensaje automático generado por el sistema de notificaciones.
"""

            logger.info(f"Sending payment notification to {recipient_email}")

            # Send notification email
            result = await self.graph_service.send_mail(
                subject=subject, message=message, recipient=recipient_email
            )

            if result:
                logger.info(
                    f"✅ Payment notification sent successfully to {recipient_email}"
                )
                return True
            else:
                logger.error(
                    f"❌ Failed to send payment notification to {recipient_email}"
                )
                return False

        except Exception as e:
            logger.error(f"Error sending payment notification: {e}", exc_info=True)
            return False

    def add_payment_keyword(self, keyword: str) -> None:
        """
        Add a new payment keyword to the detection list

        Args:
            keyword: The keyword to add (will be wrapped with word boundaries)
        """
        pattern = rf"\b{re.escape(keyword)}\b"
        if pattern not in self.payment_keywords:
            self.payment_keywords.append(pattern)
            self.payment_pattern = re.compile(
                "|".join(self.payment_keywords), re.IGNORECASE
            )
            logger.info(f"Added payment keyword: {keyword}")

    def set_notification_recipient(self, email: str) -> None:
        """
        Update the default notification recipient

        Args:
            email: The new recipient email address
        """
        self.notification_recipient = email
        logger.info(f"Updated notification recipient to: {email}")
