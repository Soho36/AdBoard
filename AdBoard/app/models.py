from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from model_utils import FieldTracker
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = CKEditor5Field('Text', config_name='extends')
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', editable=False)
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        # return f'{self.name}: {self.description[:20]}'
        return f'{self.name}'

    # def get_absolute_url(self):
    #     return f'/posts/{self.pk}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={
            'pk': self.pk
        })


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    tracker = FieldTracker(fields=['is_approved'])

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed_to_newsletter = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures a user can like a post only once

    def __str__(self):
        return f"{self.user.username} liked {self.post.name}"