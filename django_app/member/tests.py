from django.test import TestCase

from member.models import MyUser


class UserModelTest(TestCase):
    def test_user_create(self):
        user = MyUser.objects.create(email='test@test.com', nickname='test')

        user_match = MyUser.objects.first()

        self.assertEqual(user, user_match)

