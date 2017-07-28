from django.conf import settings
from django.db import models

from group.models import MyGroup
from utils.fields import CustomImageField

__all__ = (
    'Post',
    'PostLike',
)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        MyGroup,
        on_delete=models.CASCADE,
    )
    profile_img = CustomImageField(
        upload_to='post',
        blank=True,
        default_static_image='images/no_image.png'
    )
    video = models.CharField(max_length=120)
    content = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
    )

    class Meta:
        ordering = ['-pk']


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            ('post', 'user')
        )
