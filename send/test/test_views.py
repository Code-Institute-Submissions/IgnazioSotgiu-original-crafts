from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestSendViews(TestCase):

    def setUp(self):
        # create admin user
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        # create guest
        self.client = Client()

    def test_send_email_render_correct_template(self):
        response = self.client.get(reverse('send_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send/send_email.html')
