from django.test import TestCase, Client
from django.urls import reverse


class TestCheckoutViews(TestCase):

    def test_display_checkout_no_trolley_redirect_to_right_template(self):
        client = Client()
        response = client.get(reverse('view_checkout_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('products')))
