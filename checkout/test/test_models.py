from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from store.models import Category, Product
from checkout.models import CheckoutOrder, OrderLineItem


class TestCheckoutOrderModel(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        # store the password to login later
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)

        self.c = Client()
        self.c.login(username=my_admin.username, password=password)

        self.client = Client()
        self.session = self.client.session
        self.category = Category.objects.create(name='test', slug='slugtest')
        self.category1 = Category.objects.create(
            name='paint_by_numbers', slug='pby_test')
        self.category2 = Category.objects.create(
            name='accessories', slug='acc_test')
        self.product = Product.objects.create(
            category_id=1, name='product', price=19.99, selling_fast_tag=True)
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99, special_price=10.00)

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

    def test_update_total_calculate_right_total(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(round(float(order.order_total), 2), 19.99)

    def test_delivery_charges_calculated_correctly(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )
        order_line_item.save()
        order.save()

    def test_free_delivery_calculated_correctly(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(round(float(order.delivery), 2), 0.00)

    def test_grand_total_calculated_correctly(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(round(float(order.grand_total), 2), 22.99)

    def test_product_special_price_calculated_correctly(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(round(float(order.order_total), 2), 10.00)

    def test_checkoutorder_model_return_correct_value(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(str(order), order.order_number)

    def test_orderlineitem_model_return_correct_value(self):
        order = self.checkout_order
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=self.product1,
            quantity=1,
        )
        order_line_item.save()
        order.save()
        self.assertEqual(
            str(order_line_item), f'Product: {order_line_item.product.name} -\
            order {order.order_number}')
