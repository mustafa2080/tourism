from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user_profile_update'), # Assuming you want a profile update URL
    path('bookings/', views.UserBookingListView.as_view(), name='user_booking_list'),
    path('payments/', views.UserPaymentListView.as_view(), name='user_payment_list'),
    path('reviews/', views.UserReviewListView.as_view(), name='user_review_list'),
    path('notifications/', views.UserNotificationListView.as_view(), name='user_notification_list'),
    path('wishlist/', views.UserWishlistView.as_view(), name='wishlist'),
    path('wishlist/toggle/<int:tour_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    # Add other user URLs here like profile view if needed
]
