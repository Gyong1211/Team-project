from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

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
    description = models.CharField(max_length=120, blank=True, null=True)
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

    def add_tag(self, input_tag):
        if isinstance(input_tag, str):
            # 입력받은 tag가 string object인 경우
            for tag_str in input_tag.split(','):
                tag_name = tag_str.strip()
                tag, created = GroupTag.objects.get_or_create(name=tag_name)
                self.tags.add(tag)
        elif isinstance(input_tag, GroupTag):
            # 입력받은 tag가 GroupTag instance인 경우
            self.tags.add(input_tag)
        elif isinstance(input_tag, QuerySet):
            # 입력받은 tag가 QuerySet인 경우
            for tag in input_tag:
                if not isinstance(tag, GroupTag):
                    raise ValueError('입력된 QuerySet의 항목이 tag instance가 아닙니다.')
                self.tags.add(tag)
        else:
            raise ValueError('잘못된 값을 입력했습니다.')

    def remove_tag(self, input_tag):
        if isinstance(input_tag, GroupTag):
            # 입력받은 tag가 GroupTag instance인 경우
            self.tags.remove(input_tag)
        elif isinstance(input_tag, QuerySet):
            # 입력받은 tag가 QuerySet인 경우
            for tag in input_tag:
                if not isinstance(tag, GroupTag):
                    raise ValueError('입력된 QuerySet의 항목이 tag instance가 아닙니다.')
                self.tags.remove(tag)
        else:
            raise ValueError('잘못된 값을 입력했습니다.')


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
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
