from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['from_email', 'recipient_list', 'email_subject',
                  'message']
