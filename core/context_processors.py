from .models import Currency
from django.conf import settings

def currency_processor(request):
    """Add currency information to all templates"""
    # Get current currency from session or default to settings
    current_currency_code = request.session.get('currency_code', settings.DEFAULT_CURRENCY_CODE)
    
    try:
        current_currency = Currency.objects.get(code=current_currency_code)
    except Currency.DoesNotExist:
        # Fallback to USD if selected currency doesn't exist
        try:
            current_currency = Currency.objects.get(code='USD')
            request.session['currency_code'] = 'USD'
        except Currency.DoesNotExist:
            # Handle case where Currency table might be empty
            current_currency = None
    
    # Get all active currencies for the dropdown
    # Ensure we have the four required currencies: USD, EUR, GBP, EGP
    currencies = Currency.objects.filter(code__in=['USD', 'EUR', 'GBP', 'EGP'], is_active=True)
    
    return {
        'DEFAULT_CURRENCY_CODE': settings.DEFAULT_CURRENCY_CODE,
        'current_currency_code': current_currency_code,
        'current_currency': current_currency,
        'available_currencies': currencies,
    }
