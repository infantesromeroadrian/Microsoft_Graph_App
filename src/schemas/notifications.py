"""
Pydantic schemas for Microsoft Graph notifications
"""

from typing import Any

from pydantic import BaseModel, Field


class ChangeNotification(BaseModel):
    """Individual change notification from Microsoft Graph"""

    changeType: str = Field(
        ..., description="Type of change: created, updated, deleted"
    )
    clientState: str | None = Field(
        None, description="Client state if provided during subscription"
    )
    resource: str = Field(..., description="Resource that changed")
    resourceData: dict[str, Any] | None = Field(
        None, description="Additional resource data"
    )
    subscriptionExpirationDateTime: str | None = Field(
        None, description="Subscription expiration time"
    )
    subscriptionId: str = Field(..., description="ID of the subscription")
    tenantId: str = Field(..., description="Tenant ID")


class ChangeNotificationCollection(BaseModel):
    """Collection of change notifications from Microsoft Graph"""

    value: list[ChangeNotification] = Field(
        ..., description="List of change notifications"
    )
    validationTokens: list[str] | None = Field(
        None, description="Validation tokens for subscription validation"
    )


class MailDetails(BaseModel):
    """Simplified mail details"""

    id: str
    subject: str
    from_name: str
    from_address: str
    body_preview: str
    received_datetime: str | None = None
    has_attachments: bool = False
    importance: str = "normal"
