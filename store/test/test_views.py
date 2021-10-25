from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product
from reviews.models import Review


class TestHomepageView(TestCase):

    def test_display_homepage_render_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')


class TestProducts(TestCase):

    def setUp(self):
        Category.objects.create(name='test', slug='slugtest')
        self.product1 = Product.objects.create(
            category_id=1, name='product', price=19.99)

    def test_products_render_right_template(self):
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/products.html')


class TestSingleProduct(TestCase):

    def test_single_product_render_right_template(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.c = Client()
        self.c.login(username=my_admin.username, password=password)
        reviews_count = 0
        Category.objects.create(name='test', slug='slugtest')
        self.product = Product.objects.create(
            category_id=1, name='product', price=19.99)
        self.review = Review.objects.create(
            review_date='12 Sept 2021',
            product=self.product,
            review_title='test_review',
            review_text='test_text_review',
            author=my_admin,
        )
        reviews = Review.objects.all().filter(product=self.product)
        for review in reviews:
            reviews_count += 1
        response = self.client.get(f'/{self.product.id}/')
        self.assertEqual(reviews_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/single_product.html')


class TestSearchResultAndStoreViews(TestCase):

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
        self.product1 = Product.objects.create(
            category_id=1, name='product1', price=19.99, number_in_stock=0)

    def test_search_view_use_correct_template(self):
        response = self.client.get(reverse('search_result'))
        self.assertEqual(response.status_code, 200)

    def test_search_category_use_correct_template(self):
        response = self.client.get(
            reverse('search_result'), {'category': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_search_keyword_use_correct_template(self):
        response = self.client.get(
            reverse('search_result'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_search_use_correct_template(self):
        response = self.client.get(
            reverse('search_result'), {'q': ''})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(reverse('home'))

    def test_best_sellers_render_right_template(self):
        response = self.client.get(reverse('best_sellers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/best_sellers.html')

    def test_contact_page_render_right_template(self):
        response = self.client.get(reverse('contact_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/contact_page.html')

    def test_paint_by_numbers_render_right_template(self):
        response = self.client.get(reverse('paint_by_numbers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/paint_by_numbers.html')

    def test_accessories_render_right_template(self):
        response = self.client.get(reverse('accessories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/accessories.html')

    def test_original_gallery_render_right_template(self):
        response = self.client.get(reverse('original_gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/original_gallery.html')

    def test_about_render_right_template(self):
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/about_page.html')

    def test_admin_hidden_products_display_right_template(self):
        response = self.c.get(reverse('hidden_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/hidden_products.html')

    def test_no_admin_hidden_products_redirect_right_template(self):
        response = self.client.get(reverse('hidden_products'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_admin_out_of_stock_products_display_right_template(self):
        product = self.product1
        response = self.c.get(reverse('out_of_stock_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/out_of_stock_products.html')
        self.assertContains(response, product)

    def test_no_admin_out_of_stock_products_redirect_right_template(self):
        response = self.client.get(reverse('out_of_stock_products'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_admin_add_products_display_right_template(self):
        response = self.c.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/add_product.html')

    def test_no_admin_add_product_redirect_right_template(self):
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_admin_update_product_display_right_template(self):
        product = self.product
        response = self.c.get(f'/store/update/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/update_product.html')

    def test_no_admin_update_product_redirect_right_template(self):
        product = self.product
        response = self.client.get(f'/store/update/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_admin_delete_warning_display_right_template(self):
        product = self.product
        response = self.c.get(f'/store/delete_warning/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/delete_product_warning.html')

    def test_no_admin_delete_warning_redirect_right_template(self):
        product = self.product
        response = self.client.get(f'/store/delete_warning/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))

    def test_admin_delete_product_redirect_right_template(self):
        product = self.product
        response = self.c.get(f'/store/delete_product/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('products')))

    def test_no_admin_delete_product_redirect_right_template(self):
        product = self.product
        response = self.client.get(f'/store/delete_product/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('home')))
