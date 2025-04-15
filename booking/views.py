from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy # Import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Booking
from .forms import BookingForm
from tour.models import Tour # Uncommented

# Basic CRUD views using Django's generic class-based views

class BookingListView(LoginRequiredMixin, ListView):
    """
    Displays a list of bookings for the currently logged-in user.
    """
    model = Booking
    template_name = 'booking/booking_list.html' # Needs to be created
    context_object_name = 'bookings'
    paginate_by = 10 # Optional pagination

    def get_queryset(self):
        # Filter bookings to show only those belonging to the logged-in user
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')
        # Placeholder removed

class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    Displays details of a specific booking.
    Ensures the user viewing the booking is the one who made it.
    """
    model = Booking
    template_name = 'booking/booking_detail.html' # Needs to be created
    context_object_name = 'booking'

    def get_queryset(self):
        # Ensure users can only see their own bookings
        return Booking.objects.filter(user=self.request.user)
        # Placeholder removed

class BookingCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new booking.
    Associates the booking with the logged-in user and the selected tour.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html' # Needs to be created
    # success_url = reverse_lazy('booking:booking_list') # Changed below

    def form_valid(self, form):
        # Assign the logged-in user to the booking
        form.instance.user = self.request.user

        # Get the tour from the URL kwargs (assuming URL pattern includes <int:tour_id>)
        tour_id = self.kwargs.get('tour_id')
        if not tour_id:
             # Fallback: Check if tour_id is passed in POST data (e.g., hidden input)
             tour_id = self.request.POST.get('tour_id')

        if tour_id:
            tour = get_object_or_404(Tour, pk=tour_id)
            form.instance.tour = tour
        else:
            messages.error(self.request, _("Tour information is missing."))
            return self.form_invalid(form)

        # --- Price Calculation Logic ---
        # This is a basic example. Real-world scenarios might involve:
        # - Different prices for adults/children
        # - Checking against TourDate availability and pricing
        # - Applying promotions/discounts
        tour_price = tour.discount_price if tour.has_discount else tour.price
        num_adults = form.cleaned_data.get('num_adults', 1)
        num_children = form.cleaned_data.get('num_children', 0)
        # Simple price calculation (adjust as needed)
        form.instance.total_price = (tour_price * num_adults) # Add child price logic if applicable

        # --- Availability Check (Example - Needs refinement based on TourDate) ---
        # This assumes start_date links to a specific TourDate or needs validation against it
        # start_date = form.cleaned_data.get('start_date')
        # try:
        #     tour_date = TourDate.objects.get(tour=tour, start_date=start_date)
        #     required_seats = num_adults + num_children
        #     if tour_date.available_seats < required_seats:
        #         messages.error(self.request, _("Not enough available seats for the selected date."))
        #         return self.form_invalid(form)
        #     # Optionally decrease available seats here or after payment confirmation
        # except TourDate.DoesNotExist:
        #     messages.error(self.request, _("Selected date is not available for this tour."))
        #     return self.form_invalid(form)

        # Save the booking instance first to get an ID
        self.object = form.save()

        messages.success(self.request, _("Booking initiated successfully! Please proceed to payment."))
        # Redirect to payment processing view (assuming it exists)
        # Replace 'payments:process_payment' with the actual URL name
        payment_url = reverse('payments:create_payment', kwargs={'booking_id': self.object.id})
        return redirect(payment_url)
        # return super().form_valid(form) # Don't call super() if redirecting manually

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add tour information to context if creating booking from a tour page
        tour_id = self.kwargs.get('tour_id')
        if tour_id:
            context['tour'] = get_object_or_404(Tour, pk=tour_id)
        context['page_title'] = _('Create Booking')
        return context

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handles updating an existing booking.
    Restricted to the user who made the booking.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html' # Reuses the form template
    success_url = reverse_lazy('booking:booking_list')
    context_object_name = 'booking'

    def get_queryset(self):
        # Ensure users can only edit their own bookings
        return Booking.objects.filter(user=self.request.user)
        # Placeholder removed

    def form_valid(self, form):
        # Recalculate price if relevant fields changed?
        messages.success(self.request, _("Booking updated successfully."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Update Booking')
        return context

# Add a view for cancelling bookings if needed
# def cancel_booking(request, pk):
#     booking = get_object_or_404(Booking, pk=pk, user=request.user) # Ensure ownership
#     if booking.status == 'pending' or booking.status == 'confirmed':
#         booking.status = 'cancelled'
#         booking.save()
#         messages.success(request, _("Booking cancelled successfully."))
#         # Add refund logic trigger here if applicable
#     else:
#         messages.error(request, _("This booking cannot be cancelled."))
#     return redirect('booking:booking_detail', pk=pk)
