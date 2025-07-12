from celery import shared_task
from core.utils.send_sms_or_email import send_sms, send_email

# Celery task for sending SMS with retry on failure
@shared_task(bind=True, max_retries=3)
def send_sms_task(self, phone_number: str, message: str):
    """
    Sends an SMS to the given phone number using a background task.

    Retries up to 3 times if sending fails, with a 5-second delay between retries.
    """
    try:
        return send_sms(phone_number, message)
    except Exception as e:
        raise self.retry(exc=e, countdown=5)

# Celery task for sending email with retry on failure
@shared_task(bind=True, max_retries=3)
def send_email_task(self, to_email: str, subject: str, message: str):
    """
    Sends an email with the given subject and message to the specified email address.

    Retries up to 3 times if sending fails, with a 5-second delay between retries.
    """
    try:
        return send_email(to_email, subject, message)
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
