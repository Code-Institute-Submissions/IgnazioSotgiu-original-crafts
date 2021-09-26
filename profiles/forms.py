from django.forms import ModelForm
from .models import Profile

# code taken from code institute lecture


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['phone_number',
                  'street_address', 'town_or_city', 'county',
                  'country', 'zip_postcode']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'phone_number': 'Phone Number',
            'street_address': 'Address',
            'town_or_city': 'Town or City',
            'county': 'County',
            'country': 'select Country',
            'zip_postcode': 'Postcode',
        }

        # for field in self.fields:
        #     placeholder = placeholders[field]
        #     self.fields[field].widget.attrs['placeholder'] = placeholder
