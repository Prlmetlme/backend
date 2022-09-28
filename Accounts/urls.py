from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountHandlerView.as_view()),
    path('<str:id>', views.AccountHandlerView.as_view()),
    path('all/<str:pattern>', views.AccountHandlerView.as_view()),
]