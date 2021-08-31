from django.test import TestCase
from store.models import Category, Product


class test_homepage_view(TestCase):

    def test_display_homepage_render_right_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')


class test_products(TestCase):

    def setUp(self):
        Category.objects.create(name='test', slug='slugtest')
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99)

    def test_products_render_right_template(self):
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/products.html')


class test_single_product(TestCase):

    def test_single_product_render_right_template(self):
        Category.objects.create(name='test', slug='slugtest')
        product = Product.objects.create(
            category_id=1, name='product', price=19.99)
        response = self.client.get(f'/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/single_product.html')
