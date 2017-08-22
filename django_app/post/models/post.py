import time
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from group.models import MyGroup
from ..tasks import task_update_like_count

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
    comment_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def calc_like_count(self):
        time.sleep(1)
        self.like_count = self.like_users.count()
        self.save()

    def calc_comment_count(self):
        time.sleep(1)
        self.comment_count = self.comment_set.count()
        self.save()

    def __str__(self):
        return '\nauthor: {}\ncontent: {}'.format(self.author.nickname, self.content)

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
            ('post', 'user'),
        )


@receiver(post_save, sender=PostLike, dispatch_uid='postlike_save_update_like_count')
@receiver(post_delete, sender=PostLike, dispatch_uid='postlike_delete_update_like_count')
def update_like_count(sender, instance, **kwargs):
    if kwargs['signal'].receivers[1][0][0] == 'postlike_save_update_like_count':
        instance.post.like_count += 1
    else:
        instance.post.like_count -= 1
    instance.post.save()
    task_update_like_count.delay(post_pk=instance.post.pk)
