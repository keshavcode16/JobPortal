from django.urls import include, path
from rest_framework import routers
from .views import (
    ProductViewSet, 
    CommentEditHistoryAPIView,
    CommentsDestroyGetCreateAPIView, 
    CommentsListCreateAPIView,
    DislikeCommentLikesAPIView, 
    DislikesAPIView,
    FavoriteAPIView, 
    FilterAPIView, 
    LikeCommentLikesAPIView,
    LikesAPIView, 
    NotificationViewset, 
    RateAPIView,
    ReadAllNotificationViewset, 
    TagListAPIView, 
    BookmarkAPIView, 
    ProductModelResourcesViewSet,
    web_store_home_view,
    product_list_view_with_model,
    product_view_with_model
)

app_name = "web_store"

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')


web_router_v1 = routers.SimpleRouter()

router.register(r'product_model_resources', ProductModelResourcesViewSet,  basename='post_resources')
router.register(r'products', ProductViewSet,  basename='products')



urlpatterns = [
    path('api/', include(router.urls)),
    path('', web_store_home_view),
    path('<str:model_slug>', product_list_view_with_model, name='product_list_view_with_model'),
    path('product/<str:product_slug>', product_view_with_model, name='product_view_with_model'),
]