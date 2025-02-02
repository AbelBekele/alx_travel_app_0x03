from .tasks import send_booking_confirmation_email

class BookingViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    def perform_create(self, serializer):
        booking = serializer.save()
        
        # Trigger the email task asynchronously
        send_booking_confirmation_email.delay(
            booking_id=booking.id,
            user_email=booking.user.email,
            listing_title=booking.listing.title
        )
        
        return booking

# ... existing code ... 