
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
        'authentication.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=profile_image_directory_path, verbose_name="Profile Image")
    interests = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(
        'web_store.Product', symmetrical=False, blank=True, related_name='users_fav_products')
    follows = models.ManyToManyField(
        'self',
        related_name='follower',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return '{}'.format(self.user.email)

    def favorite(self, product):
        self.favorites.add(product)

    def unfavorite(self, product):
        self.favorites.remove(product)

    def follow(self, profile):
        """Follow another user if not already following"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow another user if followed"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if a user is followed by active user. False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_follower(self, profile):
        """Returns True if a user is following active user; False otherwise."""
        return self.follower.filter(pk=profile.pk).exists()
