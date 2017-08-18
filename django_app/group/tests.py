from django.test import TestCase

from group.models import MyGroup
from member.models import MyUser, Membership


class MyGroupModelTest(TestCase):
    DUMMY_USER_EMAIL = 'dummy@dummy.com'
    DUMMY_USER_PASSWORD = 'dummy'

    def test_fields_default_value(self):
        user = MyUser.objects.create_user(
            email=self.DUMMY_USER_EMAIL,
            password=self.DUMMY_USER_PASSWORD
        )

        group = MyGroup.objects.create(
            owner=user,
            name='dummy group',
            description='group create test'
        )
        # group_type 검사
        self.assertEqual(group.group_type, 'PUBLIC')
        # profile_img url 검사
        self.assertEqual(group.profile_img.url, '/static/images/no_image.png')
        # num_of_members 검사
        self.assertEqual(group.num_of_members, 1)


class MyGroupManagerTest(TestCase):
    DUMMY_USER_EMAIL = 'dummy@dummy.com'
    DUMMY_USER_PASSWORD = 'dummy'

    def test_objects_create(self):
        user = MyUser.objects.create_user(
            email=self.DUMMY_USER_EMAIL,
            password=self.DUMMY_USER_PASSWORD
        )

        group = MyGroup.objects.create(
            owner=user,
            name='dummy group',
            description='group create test'
        )
        self.assertTrue(Membership.objects.filter(user=user, group=group).exists())
