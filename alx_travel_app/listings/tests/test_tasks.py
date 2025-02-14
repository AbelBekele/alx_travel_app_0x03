from django.test import TestCase, override_settings
from django.core import mail
from django.conf import settings
from ..tasks import send_booking_confirmation_email
import logging

logger = logging.getLogger(__name__)

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True  # This makes Celery execute tasks synchronously
)
class EmailTaskTests(TestCase):
    def setUp(self):
        # Clear the test outbox before each test
        mail.outbox = []

    def test_send_booking_confirmation_email(self):
        # Test data
        booking_id = "12345"
        user_email = "itsabel77@gmail.com"
        listing_title = "Luxury Beach Villa"

        # Call the task
        result = send_booking_confirmation_email(booking_id, user_email, listing_title)

        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Get the sent email
        email = mail.outbox[0]
        
        # Check email properties
        self.assertEqual(email.subject, f'Booking Confirmation - {listing_title}')
        self.assertEqual(email.from_email, 'abelbekele.addise@gmail.com')  # Updated to match your EMAIL_HOST_USER
        self.assertEqual(email.to, [user_email])
        
        # Check email content
        expected_message = (
            f"Thank you for your booking!\n\n"
            f"Booking Details:\n- Booking ID: {booking_id}\n- Property: {listing_title}\n\n"
            "We hope you enjoy your stay!"
        )
        self.assertEqual(email.body, expected_message)
        
        # Check task return value
        self.assertEqual(result, f"Confirmation email sent for booking {booking_id}")

    def test_send_booking_confirmation_email_failure(self):
        # Test with empty email to trigger validation error
        booking_id = "12345"
        user_email = ""  # Empty email will cause validation error
        listing_title = "Luxury Beach Villa"

        # The task should raise an exception with an empty email
        with self.assertRaises(ValueError):  # Changed to ValueError which Django raises for invalid emails
            send_booking_confirmation_email(booking_id, user_email, listing_title)