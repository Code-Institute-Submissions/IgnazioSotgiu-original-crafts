from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from store.models import Category, Product
from checkout.models import CheckoutOrder


class TestProfileViews(TestCase):

    def setUp(self):
        # store the password to login later
        password = 'mypassword'

        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)

        self.c = Client()
        self.c.login(username=my_admin.username, password=password)

        self.client = Client()
        self.category = Category.objects.create(name='test', slug='slugtest')
        self.category1 = Category.objects.create(
            name='paint_by_numbers', slug='pby_test')
        self.category2 = Category.objects.create(
            name='accessories', slug='acc_test')
        self.product = Product.objects.create(
            category_id=1, name='product', price=19.99, selling_fast_tag=True)

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

    def test_profile_page_redirect_not_auth_user_to_correct_template(self):
        response = self.client.get(reverse('profile_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_profile_order_history_not_auth_user_redirect_correct_template(self):
        order = self.checkout_order
        response = self.client.get(f'/checkout_completed/{order.order_number}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))
