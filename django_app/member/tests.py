from django.test import TestCase

from member.models import MyUser, UserRelation


class UserModelTest(TestCase):
    def test_user_create(self):
        user = MyUser.objects.create(email='test@test.com', nickname='test')

        user_match = MyUser.objects.first()

        self.assertEqual(user, user_match)

        def test_userrelation(self):
            user1 = MyUser.objects.create(email='test1@test.com', nickname='test1')
            user2 = MyUser.objects.create(email='test2@test.com', nickname='test2')

            relation = UserRelation.objects.create(user1=user1, user2=user2)
            relation_m = UserRelation.objects.first()

            self.assertEqual(relation, relation_m)
            self.assertEqual(user1, relation.user1)
            self.assertEqual(user2, relation.user2)
