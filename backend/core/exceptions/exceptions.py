class MessageDeliveryError(Exception):
    """Base exception for all message delivery issues."""

class EmailSendError(MessageDeliveryError):
    """Raised when email sending fails."""

class SmsSendError(MessageDeliveryError):
    """Raised when SMS sending fails."""