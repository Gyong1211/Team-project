from django.db import models

from member.models import MyUser
from .post import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    author = models.ForeignKey(MyUser)
    content = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date',]

    def __str__(self):
        return '\n글내용: \n작성자: {}\n댓글 내용: {}'.format(self.post, self.author, self.content)