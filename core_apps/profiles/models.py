
from django.conf import settings
from django.db import models
import shortuuid

# User = settings.AUTH_USER_MODEL


def profile_image_directory_path(instance, filename):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    rnd = s.random(length=6)

    return f'profiles/images/{instance.user.id}/{rnd}-{filename}'


class Profile(models.Model):
    """This class represents the user profile model."""

    # resticting user to have one and only one profile
    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=profile_image_directory_path, verbose_name="Profile Image")
    interests = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return '{}'.format(self.user.email)
