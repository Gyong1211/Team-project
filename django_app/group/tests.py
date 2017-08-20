from django.test import TestCase

from group.models import MyGroup
from member.models import MyUser, Membership


class MyGroupModelTest(TestCase):
    DUMMY_USER_EMAIL = 'dummy@dummy.com'
    DUMMY_USER_NICKNAME = 'dummy'
    DUMMY_GROUP_NAME = 'dummy group'

    @staticmethod
    def make_user(num=None):
        if not num:
            return MyUser.objects.create(email='dummy@dummy.com', nickname='dummy')
        else:
            return [MyUser.objects.create(
                email='dummy{}@dummy.com'.format(i),
                nickname='dummy{}'.format(i)
            ) for i in range(num)]

    @staticmethod
    def make_dummy_group(user):
        return MyGroup.objects.create(owner=user, name='dummy group')

    def test_fields_default_value(self):
        user = self.make_user()
        group = self.make_dummy_group(user)

        # group_type 검사
        self.assertEqual(group.group_type, 'PUBLIC')
        # profile_img url 검사
        self.assertEqual(group.profile_img.url, '/static/images/no_image.png')
        # num_of_members 검사
        self.assertEqual(group.num_of_members, 1)

    def test_add_tag_method(self):
        user = self.make_user()
        group = self.make_dummy_group(user)
        group.add_tag('dummy')
        self.assertTrue(group.tags.filter(name='dummy').exists)


class MyGroupManagerTest(TestCase):
    DUMMY_USER_EMAIL = 'dummy@dummy.com'
    DUMMY_USER_PASSWORD = 'dummy'

    def test_create_method(self):
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
