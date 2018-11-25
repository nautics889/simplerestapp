from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """Post model contains fields below. If delete author's account, his posts aren't deleted automatically"""
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='posts')
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'post'

class Like(models.Model):
    """Like model contains only two fields which are foreign key to user and post"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'like'