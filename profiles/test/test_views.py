from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product
from checkout.models import CheckoutOrder
from django.contrib.auth import get_user_model


class TestProfileViews(TestCase):

    def setUp(self):
        # store the password to login later
        password = 'mypassword'

        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)

        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

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

    def test_profile_order_history_not_auth_use_correct_template(self):
        order = self.checkout_order
        response = self.client.get(
            f'/checkout/checkout_completed/{order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_completed.html')

    def test_profile_order_not_auth_user_email_sent_use_correct_template(self):
        order = self.checkout_order
        order.email_sent = True
        order.save()
        response = self.client.get(
            f'/checkout/checkout_completed/{order.order_number}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_profile_order_history_auth_use_correct_template(self):
        order = self.checkout_order
        order.profile = get_user_model().objects.last().profile
        order.save()
        response = self.c.get(
            f'/checkout/checkout_completed/{order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_completed.html')

    def test_profile_order_history_auth_user_email_sent_correct_template(self):
        order = self.checkout_order
        order.profile = get_user_model().objects.last().profile
        order.email_sent = True
        order.save()
        response = self.c.get(
            f'/checkout/checkout_completed/{order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'checkout/checkout_completed.html')

    # def test_auth_user_can_save_form(self):
    #     user = self.my_admin
    #     profile = {
    #         'user': user,
    #         'phone_number': '136545479',
    #         'street_address': '123 main st',
    #         'town_or_city': 'city',
    #         'zip_postcode': '12',
    #         'county': 'county',
    #     }
    #     form = ProfileForm(instance=profile)
    #     form.save()
    #     self.assertEqual(profile.user, user)
    #     self.assertEqual(user.profile.town_or_city, 'city')
    #     self.assertEqual(user.profile.county, 'county')
