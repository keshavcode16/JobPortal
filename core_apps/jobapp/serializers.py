import re

from core_apps.profiles.serializers import ProfileSerializer
from notifications.models import Notification
from rest_framework import serializers
from .models import JobPost, JobApplication
import traceback




class JobPostSerializer(serializers.ModelSerializer):
    """
    Defines the product serializer
    """
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    unit_price = serializers.CharField(max_length=200,source='unit_price.name')
    model = serializers.CharField(max_length=200,source='product_model.name')
    product_image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = JobPost
        fields = ['id', 'name', 'description',  'tagList','topics', "product_image", "created_at", "updated_at"]

    def get_favorite_count(self, instance):

        return instance.users_fav_products.count()

    def is_favorited(self, instance):
        request = self.context.get('request')
        if request is None:
            return False

        username = request.user.username
        if instance.users_fav_products.filter(user__username=username).count() == 0:
            return False

        return True

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        topics = validated_data.pop('topics', [])
        product = Product.objects.create(**validated_data)
        for tag in tags:
            product.tags.add(tag)    

        return product

    def validate(self, data):
        # The `validate` method is used to validate the title,
        # description and body
        title = data.get('title', None)
        description = data.get('description', None)
        # Validate title is not a series of symbols or non-alphanumeric characters
        if re.match(r"[!@#$%^&*~\{\}()][!@#$%^&*~\{\}()]{2,}", title):
            raise serializers.ValidationError(
                "A title must not contain two symbols/foreign characters following each other"
            )
        # Validate the description is not a series of symbols or
        # non-alphanumeric characters
        if description is not None:
            if re.match(r"[!@#$%^&*~\{\}()][!@#$%^&*~\{\}()]{2,}", description):
                raise serializers.ValidationError(
                    """
                    A description must not contain two symbols/foreign characters following each other
                    """
                )
        return data

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    def is_bookmarked(self, instance):
        request = self.context.get('request')
        if request is None:
            return False
        if Bookmarks.objects.filter(post_id=instance.id, user_id=instance.author.user_id):
            return True
        return False


