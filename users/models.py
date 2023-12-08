from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

  subscription = models.ForeignKey(
    'djstripe.Subscription', null=True, blank=True, on_delete=models.SET_NULL, default=None,
    help_text="The user's Stripe Subscription object, if it exists"
  )
  
  customer = models.ForeignKey(
    'djstripe.Customer', null=True, blank=True, on_delete=models.SET_NULL, default=None,
    help_text="The user's Stripe Customer object, if it exists"
  )

  def __str__(self):
    return f"{self.username} {self.subscription} {self.customer}"