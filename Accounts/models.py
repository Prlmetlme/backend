# from __future__ import braces
from django.contrib.auth.models import AbstractUser
from django.db import models
from misc_utils import id_generator, upload_image

class User(AbstractUser):
    birthday = models.DateField(auto_now=False, auto_created=False, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_image, null=True, blank=True)
    banner_image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    occupation = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=100)
    bio = models.TextField(blank=True)
    static_user_id = models.CharField(max_length=36, unique=True, default=id_generator, editable=False)
    is_active = models.BooleanField(auto_created=True, default=True)
    liked_posts = models.ManyToManyField('Engagements.Post', related_name='liked_by', blank=True)
    liked_comments = models.ManyToManyField('Engagements.Comment', related_name='liked_by', blank=True)
    disliked_posts = models.ManyToManyField('Engagements.Post', related_name='disliked_by', blank=True)
    disliked_comments = models.ManyToManyField('Engagements.Comment', related_name='disliked_by', blank=True)
    privated = models.BooleanField(default=False)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.last_name}, {self.first_name}'
        return self.username

