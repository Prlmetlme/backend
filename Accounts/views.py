from decouple import config
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from Serenite_API.settings import SIMPLE_JWT
from django.middleware import csrf
from django.shortcuts import get_object_or_404
from request_utils import user_from_access_token, get_engagement_data_or_400

from .serializer import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, UserSerializer, ReadUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from Accounts import serializer
from . import models
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



class AccountHandlerView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('id'):
            user_id = kwargs.get('id')
            user:models.User = get_object_or_404(models.User.objects.filter(static_user_id=user_id))
            serialized = ReadUserSerializer(user)
            print('\n\n', kwargs, '\n\n')
            return Response(serialized.data)
        elif kwargs.get('pattern'):
            pattern = kwargs.get('pattern')
            search_results = models.User.objects.filter(username__icontains=pattern)
            users = ReadUserSerializer(search_results, many=True)
            return Response(users.data)
        else:
            user:models.User = user_from_access_token(request)
            serialized = serializer.ReadUserSerializer(user)
            # user_info = {key: serailized.data[key] for key in serailized.data if (key != 'password')}
            return Response(serialized.data)

    def post(self, request):
        serialized = serializer.UserSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response({'Success': 'Account was created successfully'}, status=201)
        return Response(status=400)

    def delete(self, request):
        permission_classes = (IsAuthenticated,)
        user:models.User = user_from_access_token(request)
        user.delete()
        return Response(status=204)


class TestHTTP(APIView):
    def _get_tokens_for_user(self, user:object):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def get(self, request):
        # posts:models.Post = get_object_or_404(models.Post.objects.filter(post_ID='LV42PUVA-JDYQKURO-3A53WKR7-NHXA3NR7'))
        posts:models.Post = models.Post.objects.get(post_ID='LV42PUVA-JDYQKURO-3A53WKR7-NHXA3NR7')
        # serailized = serializer.UserSerializer(posts.liked_by.all(), many=True)
        serailized = serializer.PostSerializer(posts)
        # return Response(models.Post. liked_by.all())
        return Response(serailized.data)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        response = Response()
        user = authenticate(username=username, password=password)
        if user is not None:
            response.data = {'Success': 'Login successful'}
            return response
        else:
            return Response({'Invalid': 'Username or password does not match our records'}, status=404)




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

