from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
# Assuming 'tour' app has a 'Tour' model and 'users' app has 'CustomUser'
from tour.models import Tour # Uncommented
from users.models import CustomUser # Uncommented

class Booking(models.Model):
    """
    Represents a tour booking made by a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("User")) # Uncommented
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Tour")) # Uncommented
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Booking Date"))
    start_date = models.DateField(verbose_name=_("Start Date")) # Consider linking this to TourDate model if applicable
    end_date = models.DateField(verbose_name=_("End Date")) # Consider linking this to TourDate model if applicable
    num_adults = models.PositiveIntegerField(default=1, verbose_name=_("Number of Adults"))
    num_children = models.PositiveIntegerField(default=0, verbose_name=_("Number of Children"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Price"), blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('confirmed', _('Confirmed')),
            ('cancelled', _('Cancelled')),
            ('completed', _('Completed')),
        ],
        default='pending',
        verbose_name=_("Status")
    )
    special_requests = models.TextField(blank=True, null=True, verbose_name=_("Special Requests"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ['-booking_date']

    def calculate_price(self):
        """Calculate the total price based on tour price, number of adults and children"""
        if not self.tour:
            return 0
            
        # Get the base price from the tour
        if self.tour.discount_price is not None:
            base_price = self.tour.discount_price
        else:
            base_price = self.tour.price
            
        # Calculate total (children at half price)
        # Use Decimal for calculations to avoid type errors
        total = (base_price * self.num_adults) + (base_price * Decimal('0.5') * self.num_children)
        return total
    
    def save(self, *args, **kwargs):
        # Calculate total price if it's not set
        if not self.total_price:
            self.total_price = self.calculate_price()
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Use try-except in case tour or user is somehow missing, though FKs should prevent this
        try:
            return f"Booking for {self.tour.name} by {self.user.get_full_name()}"
        except (Tour.DoesNotExist, CustomUser.DoesNotExist):
             return f"Booking ID: {self.id} - Status: {self.get_status_display()}"

# Add related models if needed, e.g., Passenger details
# class Passenger(models.Model):
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
#     full_name = models.CharField(max_length=255)
#     date_of_birth = models.DateField()
#     # ... other relevant fields
