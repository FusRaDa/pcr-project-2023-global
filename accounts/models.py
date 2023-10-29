from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Group


# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(blank=True, upload_to='profiles/')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return (self.first_name + " " + self.last_name)

    @property
    def image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return "/images/profile-icon.png"
        
    @property
    def group_access(self):
        query = self.username.groups.values_list('name', flat=True)
        return query[0]

        
class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication
    with either a username or an email address.
    """
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None