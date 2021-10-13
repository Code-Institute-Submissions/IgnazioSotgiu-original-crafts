# from django.test import TestCase, Client
# from django.contrib.auth.models import Permission
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from checkout.models import CheckoutOrder


# class TestViewCheckoutPage(TestCase):

#     def setUp(self):

#         self.checkout_order = CheckoutOrder.objects.create(
#             order_number='',
#             full_name='test name',
#             email_address='test@example.com',
#             phone_number='01234564766',
#             street_address='main st',
#             town_or_city='dublin',
#             county='dublin',
#             zip_postcode='12',
#             order_date='12 Sept 2021',
#             delivery=0,
#             order_total=0,
#             grand_total=0,
#             order_trolley='',
#             order_pid='',
#         )

#     def test_checkout_page_redirect_to_home_with_empty_cart(self):
#         response = self.client.get(reverse('view_checkout_page'))
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed(response, 'store/products.html')
