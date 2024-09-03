from django.contrib import admin
from .models import Category, Post, Comment, Like, Subscription, Newsletter


# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscription)
admin.site.register(Newsletter)
