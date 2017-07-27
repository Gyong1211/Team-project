from django.conf import settings
from django.db import models


class MyGroupManager(models.Manager):
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        Membership.objects.get_or_create(user=obj.owner, group=obj)
        return obj


class MyGroup(models.Model):
    GROUP_TYPE = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('HIDDEN', 'Hidden'),
    )
    name = models.CharField(max_length=24)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    group_type = models.CharField(
        max_length=10,
        choices=GROUP_TYPE,
        default='PUBLIC',
    )
    profile_img = models.ImageField(null=True)
    description = models.CharField(max_length=120)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='groups_joined',
    )
    tags = models.ManyToManyField(
        'GroupTag',
    )
    objects = MyGroupManager()

    def __str__(self):
        return 'Group : {}'.format(self.name)

    def member_count(self):
        return self.members.count()


class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        MyGroup,
        on_delete=models.CASCADE
    )
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'group')
        )


class GroupTag(models.Model):
    name = models.CharField(max_length=128)
