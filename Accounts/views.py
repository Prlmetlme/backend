import base64
from decouple import config
from request_utils import user_from_access_token, get_engagement_data_or_400
from token_utils import generate_reset_password_link, verify_rest_password_link
from misc_utils import url_encode_token, url_decode_token

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from Serenite_API.settings import SIMPLE_JWT
from django.middleware import csrf
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

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




class AccountSearchView(APIView):
    def get(self, request):
        try:
            search_type = list(request.GET.keys())[0]
            value = request.GET[search_type]
        except: 
            return Response(None, 404)
        match search_type.lower():
            case 'exact_id':
                user_id = value
                user:models.User = get_object_or_404(models.User.objects.filter(static_user_id=user_id))
                serialized = ReadUserSerializer(user)
                return Response(serialized.data)
            case 'exact_username':
                return Response({'search type': f'The type of search is an exact match of {value}'})
            case 'pattern_username':
                pattern = value
                search_results = models.User.objects.filter(username__icontains=pattern)
                users = ReadUserSerializer(search_results, many=True)
                return Response(users.data)
            case _:
                return Response({'error': 'Please use an valid search type'})
        # match request.GET[search]:
            # case 'contains':
                # pass

        # if kwargs.get('id'):

        # elif kwargs.get('pattern'):
        #     
        # else:
        #     user:models.User = user_from_access_token(request)
        #     serialized = serializer.ReadUserSerializer(user)
        #     # user_info = {key: serailized.data[key] for key in serailized.data if (key != 'password')}
        #     return Response(serialized.data)


class AccountHandlerView(APIView):
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

class SelfHandlerView(APIView):
    def get(self, request):
        self_user = user_from_access_token(request)
        seralized = UserSerializer(self_user)

        return Response(seralized.data)

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


class Testing(APIView):
    def get(self, request):
        
        # send_mail(
        #     'Test',
        #     'This email is a test, please delete',
        #     config('EMAIL_USER'),
        #     ['brandonclarke2020@gmail.com'],
        #     False
        # )
        token = url_decode_token(request.GET['token'])

        return Response(token)
    def post(self, request):
        user = models.User.objects.get(static_user_id=request.data['user_ID'])
        token = generate_reset_password_link(user)
        url = f'http://localhost:3000/{url_encode_token(token)}'
        return Response({"one_time_link": url})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

