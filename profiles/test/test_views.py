from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product


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

    def test_profile_page_redirect_not_authenticated_user_to_correct_template(self):
        response = self.client.get(reverse('profile_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))
