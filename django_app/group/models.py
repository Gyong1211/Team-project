from django.conf import settings
from django.db import models

from utils.fields import CustomImageField


class MyGroupManager(models.Manager):
    def create(self, **kwargs):
        tag = kwargs.pop('tag', '')
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        Membership.objects.get_or_create(user=obj.owner, group=obj)
        obj.add_tag(tag)
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

    def add_tag(self, tag):
        if isinstance(tag, str):
            # 입력받은 tag가 string object인 경우
            for tag_name in tag.split(','):
                tag_str = tag_name.strip()
                group_tag, created = GroupTag.objects.get_or_create(name=tag_str)
                self.tags.add(group_tag)
        elif isinstance(tag, GroupTag):
            # 입력받은 tag가 GroupTag instance인 경우
            self.tags.add(tag)
        else:
            raise ValueError

    def remove_tag(self, tag):
        if not isinstance(tag, GroupTag):
            raise ValueError

        self.tags.remove(tag)


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
