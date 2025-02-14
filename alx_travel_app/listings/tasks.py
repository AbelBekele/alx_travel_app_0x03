from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
import logging
from celery.exceptions import MaxRetriesExceededError
from smtplib import SMTPException
import os

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def send_booking_confirmation_email(self, booking_id, user_email, listing_title, check_in_date=None, check_out_date=None, guest_name=None):
    """
    Send booking confirmation email with retry logic using an HTML template for the email body.
    """
    logger.info(f"Starting email task for booking {booking_id} to {user_email}")
    
    if not user_email:
        logger.error("Email validation failed: Empty email address")
        raise ValueError("Email address cannot be empty")
    
    try:
        validate_email(user_email)
        
        # Create email content (plain text fallback)
        subject = f'Booking Confirmation - {listing_title}'
        message = (
            f"Thank you for your booking!\n\n"
            f"Booking Details:\n"
            f"- Booking ID: {booking_id}\n"
            f"- Property: {listing_title}\n"
            f"- Check-in: {check_in_date}\n"
            f"- Check-out: {check_out_date}\n\n"
            "We hope you enjoy your stay!"
        )
        
        # Render the HTML template with context data
        context = {
            'booking_id': booking_id,
            'listing_title': listing_title,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'guest_name': guest_name,
        }
        template_path = os.path.join('emails', 'booking_confirmation.html')
        html_message = render_to_string(template_path, context)
        
        logger.info(f"Attempting to send email to {user_email}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Email sent successfully to {user_email}")
        return f"Confirmation email sent for booking {booking_id}"
        
    except (SMTPException, ConnectionError) as exc:
        try:
            logger.warning(f"Email sending failed, attempting retry {self.request.retries + 1} of 3")
            raise self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for sending email to {user_email}")
            raise
    except ValidationError as e:
        logger.error(f"Email validation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
        raise
