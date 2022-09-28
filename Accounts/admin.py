from django.contrib import admin
from .models import User
from Engagements.models import Comment, Post

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)