import re
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import authenticate, user_logged_in, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from homedecor.settings.base import SIMPLE_JWT as api_settings
from django.utils import timezone
from core_apps.authentication.module.GoogleAuth import GoogleAuth
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name','last_name', 'password', 'token']

    def validate(self, data):
        password = data.get('password', None)

        # Validate password has at least one small and capital letter
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z]).*", password):
            raise serializers.ValidationError(
                'A password must contain atleast one small letter and one capital letter.'
            )
        # Validate the password has atleast one number
        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                'A password must contain atleast one number.'
            )

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        if not user.is_verified:
            raise serializers.ValidationError(
                'Please verify your email.'
            )
        refresh = RefreshToken.for_user(user)    
        return {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'user_role'
        )



class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}

        if api_settings["ROTATE_REFRESH_TOKENS"]:
            if api_settings["BLACKLIST_AFTER_ROTATION"]:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()

            try:
                user = User.objects.get(id=refresh['user_id'])
                user.last_login = timezone.now()
                user.save()
                print(user.last_login)
            except Exception as e:
                pass

            data['refresh'] = str(refresh)

        return data


class GoogleAuthSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        new_user = False
        user_token = validated_data.get("user_token")
        user_id, email, firstname, lastname = GoogleAuth.auth(
            user_token=user_token)
        
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = User.objects.create_user_from_google(
                email=email,
                firstname=firstname,
                lastname=lastname,
                google_user_id=user_id
            )
            new_user = True
        return user, new_user