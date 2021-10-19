from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product
from checkout.forms import CheckoutForm
from checkout.models import CheckoutOrder, OrderLineItem


class TestCheckoutViews(TestCase):

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
            category_id=1, name='product', price=19.99)

        form_info = {
            'full_name': 'test name',
            'email_address': 'test_address',
            'phone_number': 'test_phone_number',
            'street_address': 'test_street_address',
            'town_or_city': 'test_city',
            'county': 'test county',
            'country': 'test country',
            'zip_postcode': '12',
        }

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
        self.checkout_form = CheckoutForm(form_info)

    def test_display_checkout_no_trolley_redirect_to_right_template(self):
        response = self.client.get(reverse('view_checkout_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('products')))

    # def test_checkout_page_display_correct_template(self):
    #     # form = self.checkout_form
    #     order = self.checkout_order
    #     # order.order_trolley = {"1": 1, "2": 1}
    #     self.session = self.client.session
    #     self.session['trolley.items'] = {"1": 1, "2": 1}
    #     order.order_trolley = self.session
    #     order.save()
    #     response = self.client.post(
    #         reverse('checkout_completed', args=[order.order_number]),
    #         # form,
    #     )
    #     self.assertEqual(order.order_total, 2000)
    #     self.assertEquals(order.delivery, 0)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, (reverse(f'checkout_completed/{order.order_number}')))

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
