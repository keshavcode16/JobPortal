import re

from core_apps.profiles.serializers import ProfileSerializer
from notifications.models import Notification
from rest_framework import serializers
from .models import Product, ProductModel, Bookmarks, Comment, Ratings, Tag, CommentEditHistory
from .tag_relations import TagRelatedField
import traceback



class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    reply_set = RecursiveSerializer(many=True, read_only=True)
    comment_likes = serializers.SerializerMethodField()
    comment_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'comment_likes',
            'comment_dislikes',
            'body',
            'reply_set',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        product = self.context['product']
        author = self.context['author']
        parent = self.context.get('parent', None)
        return Comment.objects.create(
            author=author, product=product, parent=parent, **validated_data
        )

    def get_comment_likes(self, obj):
        return obj.comment_likes.count()

    def get_comment_dislikes(self, obj):
        return obj.comment_dislikes.count()

    def is_edited(self):
        return False

class ProductSerializer(serializers.ModelSerializer):
    """
    Defines the product serializer
    """
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    comments = CommentSerializer(read_only=True, many=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')
    unit_price = serializers.CharField(max_length=200,source='unit_price.name')
    model = serializers.CharField(max_length=200,source='product_model.name')
    product_image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Product
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



class RatingSerializer(serializers.Serializer):
    """
    Defines the product rating serializer
    """

    rating = serializers.IntegerField(required=True)

    class Meta:
        model = Ratings
        fields = ['rating', 'total_rating', 'raters']

    def validate(self, data):
        # The `validate` method is used to validate the title, description and body
        # provided by the user during creating or updating an post
        rate = data.get('rating')

        # validate the rate is not a string but an integer or an empty value
        if isinstance(rate, str) or rate is None:
            raise serializers.ValidationError(
                """A valid integer is required."""
            )

        # validate the rate is within range
        if rate > 5 or rate < 1:
            raise serializers.ValidationError(
                """Rate must be a value between 1 and 5"""
            )

        return {"rating": rate}


class TagSerializer(serializers.ModelSerializer):
    """
    Defines the tag serializer
    """
    class Meta:
        model = Tag
        fields = ('tag',)

        def to_representation(self, obj):
            return obj.tag



class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, Post):
            serializer = ProductSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    """
    Defines the notifications serializer
    """

    class Meta:
        model = Notification
        fields = ['id', 'unread', 'verb',
                  'level', 'timestamp', 'data', 'emailed', 'recipient']


class UpdateCommentSerializer(serializers.Serializer):
    """
    Defines the update comment serializer
    """
    body = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('body', 'created_at')

    def update(instance, data):
        instance.body = data.get('body', instance.body)
        instance.save()
        return instance


class CommentEditHistorySerializer(serializers.Serializer):
    """
    Defines the create comment history serializer
    """
    body = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CommentEditHistory
        fields = ('body', 'created_at', 'updated_at')



class ProductModelSerializer(serializers.ModelSerializer):
    # thread_id = serializers.CharField(max_length=200,source='post_thread.thread_id')

    class Meta:
        model = ProductModel
        fields = (
            'id',
            'name',
            'model_slug',
            'color',
            'color_code',
            'description',
            'model_image',
            'unit_price',
            'is_draft',
            'updated_at',
            'created_at'
        )

