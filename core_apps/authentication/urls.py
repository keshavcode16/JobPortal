from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, Activate, Reset, TokenRefreshView, GoogleAuthViewSet, UserAPIView
)
app_name = 'authentication'
urlpatterns = [
    path('users/create', RegistrationAPIView.as_view(), name="register"),
    path('users/login', LoginAPIView.as_view(),name='login'),
    path('activate/<uidb64>/<token>', Activate.as_view(), name="activate"),
    path('users/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/google', GoogleAuthViewSet.as_view(), name='google_login'),
    path('users/<int:userId>', UserAPIView.as_view(),name='user_detail'),
]
