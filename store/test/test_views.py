from django.test import TestCase


class test_homepage_view(TestCase):

    def test_display_homepage_render_right_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
