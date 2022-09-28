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
        exclude = ('id', 'groups', 'user_permissions', 'password')






class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
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