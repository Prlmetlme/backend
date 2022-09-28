"""Serenite_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework_simplejwt.views import TokenVerifyView
from django.http import HttpResponse
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from Accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verification/', TokenVerifyView.as_view(), name='token_verification'),
    path('accounts/', include('Accounts.urls')),
    path('engagements/', include('Engagements.urls')),
    # path('test/', views.Test),
    path('readonly/', views.TestHTTP.as_view()),
    # path('userpost/', views.UserPostHandler.as_view()),
    # path('userpost/<str:id>', views.UserPostHandler.as_view()),
    # path('likes/', views.UserLikesHandler.as_view()),
    path('testing_manytomanyfield/', views.TestHTTP.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
