from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import CustomUser
from .forms import UserProfileForm
from booking.models import Booking
from payments.models import Payment
from reviews.models import Review
from core.models import Notification
from tour.models import Tour
from .models import WishlistItem

class UserDashboardView(LoginRequiredMixin, TemplateView):
    """Displays the main user dashboard."""
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['recent_bookings'] = Booking.objects.filter(user=user).order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.filter(booking__user=user).order_by('-created_at')[:5]
        context['recent_reviews'] = Review.objects.filter(user=user).order_by('-created_at')[:5]
        context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
        # Add more context as needed (e.g., profile completion status)
        return context

class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Allows users to update their profile information."""
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('user_profile') # Redirect back to profile page
    success_message = _("Your profile has been updated successfully.")

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Update Profile")
        return context

class UserBookingListView(LoginRequiredMixin, ListView):
    """Displays a list of the user's bookings."""
    model = Booking
    template_name = 'users/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class UserPaymentListView(LoginRequiredMixin, ListView):
    """Displays a list of the user's payments."""
    model = Payment
    template_name = 'users/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        # Assuming Payment model has a ForeignKey to Booking, which has a ForeignKey to User
        return Payment.objects.filter(booking__user=self.request.user).order_by('-created_at')

class UserReviewListView(LoginRequiredMixin, ListView):
    """Displays a list of the user's reviews."""
    model = Review
    template_name = 'users/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created_at')

class UserNotificationListView(LoginRequiredMixin, ListView):
    """Displays a list of the user's notifications."""
    model = Notification
    template_name = 'users/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 15

    def get_queryset(self):
        # Mark notifications as read when viewed? Optional.
        # Notification.objects.filter(user=self.request.user, is_read=False).update(is_read=True)
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# Add views for password change, email change etc. using django-allauth views or custom ones


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from tour.models import Tour
from .models import WishlistItem

@login_required
def toggle_wishlist(request, tour_id):
    """Add or remove a tour from the user's wishlist"""
    tour = get_object_or_404(Tour, id=tour_id)
    wishlist_item = WishlistItem.objects.filter(user=request.user, tour=tour).first()
    
    if wishlist_item:
        # Remove from wishlist
        wishlist_item.delete()
        messages.success(request, _("Tour removed from your wishlist."))
    else:
        # Add to wishlist
        WishlistItem.objects.create(user=request.user, tour=tour)
        messages.success(request, _("Tour added to your wishlist."))
    
    # Redirect back to the tour detail page
    return redirect('tour:tour_detail', slug=tour.slug)


class UserWishlistView(LoginRequiredMixin, ListView):
    """Display the user's wishlist"""
    model = WishlistItem
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist_items'
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


def user_dashboard(request):
    """User dashboard view showing upcoming bookings and completed tours"""
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    # Get current date for comparison
    today = timezone.now().date()
    
    # Get upcoming bookings (where tour end date is in the future)
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        tour__end_date__gte=today,
        status__in=['confirmed', 'pending']
    ).order_by('tour__start_date')
    
    # Get completed tours (where tour end date is in the past)
    completed_tours = Booking.objects.filter(
        user=request.user,
        tour__end_date__lt=today,
        status='confirmed'
    ).order_by('-tour__end_date')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'completed_tours': completed_tours,
    }
    
    return render(request, 'users/dashboard.html', context)
