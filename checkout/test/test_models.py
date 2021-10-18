from django.test import TestCase
from checkout.models import CheckoutOrder


class TestCheckoutOrderModel(TestCase):

    def setUp(self):
        self.checkout_order = CheckoutOrder.objects.create(
            order_number='',
            full_name='test test',
            email_address='email@example.ie',
            phone_number='0123456789',
            street_address='123 main street',
            town_or_city='town',
            county='county_test',
            zip_postcode='01234',
            order_date='25 Sept 2021',
            delivery=0,
            order_total=0,
            grand_total=0,
            order_trolley='{}',
            order_pid='1',
        )

    def test_checkout_order_model_name_field(self):
        self.assertEqual(self.checkout_order.full_name, 'test test')

    def test_order_number_is_created_if_left_blank(self):
        self.assertNotEqual(self.checkout_order.order_number, '')
