from datetime import datetime, timedelta
import jwt
import django
from django.conf import settings
from django.http.response import HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from requests.exceptions import HTTPError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth import authenticate, user_logged_in, get_user_model

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, RegistrationSerializer, CustomTokenRefreshSerializer, GoogleAuthSerializer, UserSerializer)
from .verification import SendEmail, account_activation_token
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
logger = logging.getLogger("loggers")
import traceback




django.utils.encoding.force_text = force_str


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = CustomTokenRefreshSerializer


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        SendEmail().send_verification_email(user.get('email', None), request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Activate(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account')
        else:
            return HttpResponse('Activation link is invalid!')


class Reset(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_reset = True
            user.save()

            encode_mail = urlsafe_base64_encode(
                force_bytes(user.email)).decode('utf-8')
            return Response({"token": encode_mail})
        else:
            return Response({"msg": "Error"})


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        
        try:
            user = request.data.get('user', {})
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error(traceback.print_exc())
            return Response({"error":1,"message":f"Error in Login {str(err)}"}, status=status.HTTP_404_NOT_FOUND)


class UserAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request, userId):
        try:
            user_object =  User.objects.get(id=userId)
            serializer = self.serializer_class(user_object)
            return Response({"user" : serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error":1,"message":"Given User does not exists."}, status=status.HTTP_404_NOT_FOUND)
        
        


class GoogleAuthViewSet(CreateAPIView):
    """
    Endpoint for Auth with Google
    """
    permission_classes = (AllowAny,)
    serializer_class = GoogleAuthSerializer
    queryset = None

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)
            user, new_user = serializer.save()
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                user_logged_in.send(sender=type(
                    user), request=request, user=user)
                return Response({
                    'email':user.email,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token), 'new_user': new_user})
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({"message": "Invalid Token","error":1}, status=404)

