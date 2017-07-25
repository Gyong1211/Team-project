from django.conf import settings
from django.db import models


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
    )
    profile_img = models.ImageField(null=True)
    description = models.CharField(max_length=120)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='joined_groups',
    )


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
