from rest_framework import serializers

# my local imports
from .models import Profile



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
        fields = ('id', 'first_name', 'last_name', 'email', 'bio', 'image')
        read_only_fields = ('email',)

    
    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        if instance.user:
            data.update({'username':instance.user.username})
        return data