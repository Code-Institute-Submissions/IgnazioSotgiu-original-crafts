from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Review
from store.models import Product, Category


class TestReviewModel(TestCase):

    def test_review_model_str(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        Category.objects.create(name='test', slug='slugtest')
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99)
        review = Review.objects.create(
            product=self.product1,
            review_title='test',
            review_text='test text',
            author=my_admin
        )
        self.assertEqual(str(review), 'test')
