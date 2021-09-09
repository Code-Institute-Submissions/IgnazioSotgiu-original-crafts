from django.test import TestCase
from store.models import Product, Category


class TestTrolleyView(TestCase):

    def setUp(self):
        Category.objects.create(name='test', slug='slugtest')
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99)

    def test_display_view_trolley_right_template(self):
        response = self.client.get('/trolley/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trolley/view_trolley.html')

    def test_can_add_item_to_trolley(self):
        product = self.product1
        response = self.client.post('add/', {'product_id': product.id})
        self.assertRedirects(response, 'view_trolley')
