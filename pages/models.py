from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    Body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title