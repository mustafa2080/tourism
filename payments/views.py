from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from booking.models import Booking

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'payments/process.html', {'booking': booking})

@login_required
def payment_success(request):
    return render(request, 'payments/success.html')

@login_required
def payment_failed(request):
    return render(request, 'payments/failed.html')

@csrf_exempt
def stripe_webhook(request):
    return HttpResponse(status=200)

@csrf_exempt
def paypal_webhook(request):
    return HttpResponse(status=200)
