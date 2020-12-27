from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    crdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    crdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}:{self.post.id}"
