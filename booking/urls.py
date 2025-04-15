from django.urls import path
from . import views

app_name = 'booking' # Define the namespace

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    # Path for creating a booking, linked from a specific tour
    path('new/tour/<int:tour_id>/', views.BookingCreateView.as_view(), name='booking_create'), # Renamed from booking_create_for_tour
    # path('new/', views.BookingCreateView.as_view(), name='booking_create_generic'), # Removed generic path for now
    path('<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    # path('<int:pk>/cancel/', views.cancel_booking, name='booking_cancel'), # Uncomment if cancel_booking view is added
]
