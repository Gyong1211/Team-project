from django.conf import settings
from django.db import models

from utils.fields import CustomImageField


class MyGroupManager(models.Manager):
    def create(self, **kwargs):
        tag_list = kwargs.pop('tag', '')
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        Membership.objects.get_or_create(user=obj.owner, group=obj)
        if tag_list:
            for tag_str in tag_list.split(','):
                tag = tag_str.strip()
                group_tag, created = GroupTag.objects.get_or_create(name=tag)
                obj.tags.add(group_tag)
        return obj


class MyGroup(models.Model):
    GROUP_TYPE = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('HIDDEN', 'Hidden'),
    )
    name = models.CharField(
        max_length=24,
        unique=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    group_type = models.CharField(
        max_length=10,
        choices=GROUP_TYPE,
        default='PUBLIC',
    )
    profile_img = CustomImageField(
        upload_to='group',
        blank=True,
        default_static_image='images/no_image.png'
    )
    description = models.CharField(max_length=120)
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='groups_joined',
    )
    num_of_members = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(
        'GroupTag',
    )
    objects = MyGroupManager()

    def __str__(self):
        return 'Group : {}'.format(self.name)

    def calc_num_of_members(self):
        self.num_of_members = self.member.count()
        self.save()
        return self.num_of_members


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
