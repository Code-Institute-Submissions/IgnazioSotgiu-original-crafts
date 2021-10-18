from django.test import TestCase
from send.models import Contact


class TestSendModel(TestCase):

    def test_model_str(self):

        contact = Contact.objects.create(
            from_email='test@email.com',
            recipient_list='test1@gmail.com',
            email_subject='test',
            message='test text'
        )
        self.assertEqual(str(contact), 'test')
