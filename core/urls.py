from django.urls import path
from django.views.i18n import set_language  # Add this import
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('terms/', views.TermsConditionsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='newsletter_subscribe'),
    # path('i18n/setlang/', set_language, name='set_language'), # Removed, defined globally in project urls.py
    path('set-currency/', views.set_currency, name='set_currency'),
    path('api/exchange-rates/', views.get_exchange_rates, name='get_exchange_rates'),
]
