from django.db import models
from misc_utils import id_generator, upload_image
from Accounts.models import User

class Post(models.Model):
    title = models.CharField(max_length=75)
    tldr = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    picture = models.ImageField(upload_to=upload_image, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_editted = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    author = models.ForeignKey('Accounts.User', null=True, on_delete=models.SET_NULL, to_field="static_user_id")
    post_ID = models.CharField(max_length=36, unique=True, default=id_generator, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Accounts.User', null=True, on_delete=models.SET_NULL)
    post_commented_on = models.ForeignKey('Engagements.Post', null=True, on_delete=models.SET_NULL)
    edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(auto_now=True)
    comment_ID = models.CharField(max_length=36, unique=True, primary_key=True, default=id_generator, editable=False)