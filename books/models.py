from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='не продано')


class Post(models.Model):
    STATUS_CHOICES = (
        ('обмен', 'Обмен'),
        ('аренда', 'Аренда'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField()
    number = models.IntegerField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'/format(self.name, self.post)