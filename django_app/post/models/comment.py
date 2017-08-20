from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from member.models import MyUser
from .post import Post
from ..tasks import task_update_comment_count

__all__ = (
    'Comment',
)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    author = models.ForeignKey(MyUser)
    content = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date', ]

    def __str__(self):
        return '\n글내용: \n작성자: {}\n댓글 내용: {}'.format(self.post, self.author, self.content)


@receiver(post_save, sender=Comment, dispatch_uid='comment_save_update_comment_count')
@receiver(post_delete, sender=Comment, dispatch_uid='comment_delete_update_comment_count')
def update_comment_count(sender, instance, **kwargs):
    print(kwargs['signal'].receivers)
    if kwargs['signal'].receivers[2][0][0] == 'comment_save_update_comment_count':
        instance.post.comment_count += 1
    else:
        instance.post.comment_count -= 1
    print(instance.post.comment_count)
    instance.post.save()
    task_update_comment_count.delay(post_pk=instance.post.pk)
