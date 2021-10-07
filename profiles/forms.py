from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['phone_number',
                  'street_address', 'town_or_city', 'county',
                  'country', 'zip_postcode']
