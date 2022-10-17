from django.urls import path
from . import views


urlpatterns = [
  path('likes/', views.LikesHandler.as_view()),
  path('comments/', views.CommentsHandler.as_view()),
  path('posts/', views.UserPostHandler.as_view(), name='posts'),
]