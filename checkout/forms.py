from django.forms import ModelForm
from .models import CheckoutOrder


class CheckoutForm(ModelForm):

    class Meta:
        model = CheckoutOrder
        fields = ['full_name', 'email_address', 'phone_number',
                  'street_address', 'town_or_city', 'county',
                  'country', 'zip_postcode']
