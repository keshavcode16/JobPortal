from rest_framework import serializers

# my local imports
from .models import Profile



class NewProfileSerializer(serializers.ModelSerializer):
    """This class contains a serializer for the Profile model"""

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'bio', 'image')
        read_only_fields = ('email',)



class ProfileSerializer(serializers.ModelSerializer):
    """This class contains a serializer for the Profile model"""

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.CharField(allow_blank=True, required=False)
    interests = serializers.CharField(allow_blank=True, required=False)
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'bio', 'image', 'interests', 'following')
        read_only_fields = ('email',)

    def get_following(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followed = instance

        return follower.is_following(followed)
    
    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        data.update({'followers':[], 'username': None})
        followers = instance.follows.all()
        if followers:
            serializer = NewProfileSerializer(followers,many=True)
            data.update({'followers':serializer.data})
        if instance.user:
            data.update({'username':instance.user.username})
        return data