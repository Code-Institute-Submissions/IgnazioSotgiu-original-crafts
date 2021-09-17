from django.forms import ModelForm
from .models import CheckoutOrder


class CheckoutForm(ModelForm):

    class Meta:
        model = CheckoutOrder
        fields = ['full_name', 'email_address',
                  'street_address', 'town_or_city', 'county',
                  'country', 'zip_postcode']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email_address': 'Contact Email',
            'street_address': 'Address',
            'town_or_city': 'Town or City',
            'county': 'County',
            'country': 'select Country',
            'zip_postcode': 'Postcode',
        }

        # self.fields['deliver_to_name'].attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
