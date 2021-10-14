from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from store.models import Category, Product
from reviews.models import Review


class TestReviewsViews(TestCase):

    def setUp(self):
        # create admin user
        password = 'mypassword'
        self.my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.c = Client()
        self.c.login(username=self.my_admin.username, password=password)

        # create guest
        self.client = Client()

        reviews_count = 0
        Category.objects.create(name='test', slug='slugtest')
        self.product = Product.objects.create(
            category_id=1, name='product', price=19.99)
        self.review = Review.objects.create(
            review_date='12 Sept 2021',
            product=self.product,
            review_title='test_review',
            review_text='test_text_review',
            author=self.my_admin,
        )
        reviews = Review.objects.all().filter(product=self.product)
        for review in reviews:
            reviews_count += 1

    def test_add_review_render_correct_template(self):
        product = self.product
        response = self.c.get(f'/reviews/reviews/add_review/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add_review.html')

    def test_add_review_not_registered_user_redirect_correct_template(self):
        product = self.product
        response = self.client.get(
            f'/reviews/reviews/add_review/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_edit_review_render_correct_template(self):
        product = self.product
        response = self.c.get(f'/reviews/reviews/edit_review/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')

    def test_edit_review_not_registered_user_redirect_correct_template(self):
        product = self.product
        response = self.client.get(
            f'/reviews/reviews/edit_review/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_delete_review_warning_render_correct_template(self):
        product = self.product
        response = self.c.get(
            f'/reviews/reviews/delete_review_warning/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/delete_review_warning.html')

    def test_delete_review_warning_not_registered_user_redirect_correct_template(self):
        product = self.product
        response = self.client.get(
            f'/reviews/reviews/delete_review_warning/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_not_registered_user_delete_review_redirect_right_template(self):
        product = self.product
        response = self.client.get(
            f'/reviews/reviews/delete_review/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_author_to_delete_review_redirect_right_template(self):
        product = self.product
        response = self.c.get(
            f'/reviews/reviews/delete_review/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('profile_page')))

    def test_registered_user_no_author_delete_review_redirect_right_template(self):
        user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='12345',
        )
        test_user = Client()
        test_user.login(username=user.username, password='12345')
        product = self.product
        response = test_user.get(
            f'/reviews/reviews/delete_review/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('profile_page')))

    def test_registered_user_no_author_delete_review_warning_redirect_right_template(self):
        user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='12345',
        )
        test_user = Client()
        test_user.login(username=user.username, password='12345')
        product = self.product
        response = test_user.get(
            f'/reviews/reviews/delete_review_warning/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('profile_page')))
