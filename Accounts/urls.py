from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.AccountHandlerView.as_view(), name='register_or_delete'),
    path('self/', views.SelfHandlerView.as_view(), name='register_or_delete'),
    # path('<str:id>', views.AccountHandlerView.as_view()),
    path('search/', views.AccountSearchView.as_view(), name='search'),
    path('password_reset/', views.Testing.as_view(), name='password_reset'),
]