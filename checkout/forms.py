from django.forms import ModelForm
from .models import CheckoutOrder

# code taken from code institute lecture


class CheckoutForm(ModelForm):

    class Meta:
        model = CheckoutOrder
        fields = ['full_name', 'email_address', 'phone_number',
                  'street_address', 'town_or_city', 'county',
                  'country', 'zip_postcode']

    # def __init__(self, *args, **kwargs):
    #     """
    #     Add placeholders and classes, remove auto-generated
    #     labels and set autofocus on first field
    #     """
    #     super().__init__(*args, **kwargs)
    #     placeholders = {
    #         'full_name': 'Full Name',
    #         'email_address': 'Contact Email',
    #         'phone_number': 'Phone Number'
    #         'street_address': 'Address',
    #         'town_or_city': 'Town or City',
    #         'county': 'County',
    #         'country': 'select Country',
    #         'zip_postcode': 'Postcode',
    #     }

    #     # for field in self.fields:
    #     #     if self.fields[field].required:
    #     #         placeholder = f'{placeholders[field]} *'
    #     #     else:
    #     #         placeholder = placeholders[field]
