from django.test import TestCase

from store.models import Category, Product


class TestCategoryModel(TestCase):

    def test_category_model_name_field(self):
        category = Category.objects.create(name='test')
        self.assertEqual(str(category), 'test')

    def test_category_model_friendly_name_field(self):
        f_name = Category.objects.create(name='test', friendly_name='friendly')
        self.assertEqual(Category.get_friendly_name(f_name), 'friendly')


class TestProductModel(TestCase):

    def test_product_model_name(self):
        Category.objects.create(name='test', slug='slugtest')
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99)
        product = self.product1
        self.assertEqual(str(product), 'product')
