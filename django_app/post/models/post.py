from django.conf import settings
from django.db import models

from group.models import MyGroup

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
    image = models.ImageField(
        upload_to='post',
        blank=True,
        null=True,
    )
    video = models.CharField(
        max_length=120,
        blank=True,
        null=True,
    )
    content = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
    )
    like_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def calc_like_count(self):
        self.like_count = self.like_users.count()
        self.save()

    def __str__(self):
        return '\n작성자: {}\n내용: {}'.format(self.author, self.content)

    class Meta:
        ordering = ['-created_date']


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
