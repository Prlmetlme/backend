from dataclasses import field
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.conf import settings
import datetime
from .models import User

from Accounts import models

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'

class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'groups', 'user_permissions', 'password', 'disliked_posts', 'disliked_comments', 'liked_posts', 'liked_comments')

class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'date_joined', 'static_user_id', 'last_active', 'last_login']





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs:dict):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        username = attrs.get('username')
        user:User = User.objects.get(username=username)
        user.last_login = datetime.datetime.utcnow().isoformat() + 'Z'
        user.last_active = datetime.datetime.utcnow().isoformat() + 'Z'
        user.save()
        access_token_lifetime:datetime.timedelta = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        refresh_token_lifetime:datetime.timedelta = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        data.update({ 'access_lifetime_seconds': access_token_lifetime.total_seconds() })
        data.update({ 'refresh_lifetime_seconds': refresh_token_lifetime.total_seconds() })
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        access_token_lifetime:datetime.timedelta = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        data.update({ 'access_lifetime_seconds': access_token_lifetime.total_seconds() })
        return data