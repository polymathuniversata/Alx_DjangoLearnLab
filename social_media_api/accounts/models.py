from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os


def user_profile_picture_path(instance, filename):    
    return os.path.join('profile_pics', f'user_{instance.id}', filename)


class CustomUser(AbstractUser):
    """Custom user model for the social media application."""
    
    # Additional fields
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to=user_profile_picture_path,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    website = models.URLField(_('website'), max_length=200, blank=True)
    
    # Following relationships - followers field as required by task
    followers = models.ManyToManyField(
        'self',
        through='UserFollowing',
        related_name='following',
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def follower_count(self):
        """Return the number of followers."""
        return self.following.count()
    
    @property
    def following_count(self):
        """Return the number of users being followed."""
        return self.followers.count()


class UserFollowing(models.Model):
    """Intermediate model for user following relationships."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_following_set',
        on_delete=models.CASCADE
    )
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_followers_set',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following_user'],
                name='unique_followers'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following_user')),
                name='no_self_follow'
            )
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} follows {self.following_user}"
