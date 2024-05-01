from django.urls import path

#my local imports
from .views import ProfileRetrieveAPIView, UserFollowAPIView, \
    FollowersRetrieve, FollowingRetrieve, FollowersRetrieveAPIView


app_name = 'profiles'

urlpatterns = [
    path('profiles/<username>/', ProfileRetrieveAPIView.as_view(), name='profile_view'),
    path('profiles/<username>/<actionType>/', UserFollowAPIView.as_view()),
    path('followers/', FollowersRetrieveAPIView.as_view()),
    path('following/', FollowingRetrieve.as_view()),
]
