# from django.test import TestCase
# from django.shortcuts import get_object_or_404
# from checkout.models import CheckoutOrder


# class TestCheckoutOrderModel(TestCase):

#     def setUp(self):
#         self.checkout_order = CheckoutOrder.objects.create(
#             order_number='',
#             full_name='test test',
#             email_address='email@example.ie',
#             phone_number='0123456789',
#             street_address='123 main street',
#             town_or_city='town',
#             county='county_test',
#             zip_postcode='01234',
#             order_date='25 Sept 2021',
#             delivery=0,
#             order_total=0,
#             grand_total=0,
#             order_trolley='',
#             order_pid='',
#         )

#     def test_checkout_order_model_name_field(self):
#         order = get_object_or_404(
#             CheckoutOrder, self.checkout_order.full_name == 'test test')
#         print(order)
#         order_number = order.order_number
#         self.assertFalse(order_number, '')
