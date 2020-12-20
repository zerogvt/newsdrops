from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    link = models.URLField()
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    crdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
