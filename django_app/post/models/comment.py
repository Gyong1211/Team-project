from django.db import models

from member.models import MyUser
from .post import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(MyUser)
    content = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
