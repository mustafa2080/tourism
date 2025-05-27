from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Original payment process
    path('process/<int:booking_id>/', views.process_payment, name='process'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),

    # PayPal specific (original)
    path('paypal/create/<int:booking_id>/', views.create_paypal_order, name='create_paypal_order'),
    path('paypal/capture/', views.capture_paypal_payment, name='capture_paypal_payment'),
    path('paypal/return/', views.paypal_return, name='paypal_return'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),

    # Webhooks
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('webhook/paypal/', views.paypal_webhook, name='paypal_webhook'),

    # Direct payment process (consolidated implementation)
    path('direct/<int:booking_id>/', views.payment_page, name='payment_direct'),
    path('confirm/', views.payment_confirm, name='payment_confirm'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]
