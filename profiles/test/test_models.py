from django.test import TestCase
from django.contrib.auth import get_user_model


class TestProfileModel(TestCase):

    def test_profile_model_str(self):
        get_user_model().objects.create(
            username='myuser'
        )
        profile = get_user_model().objects.last().profile
        self.assertEqual(str(profile), 'myuser')
