from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
  company = models.CharField(blank=False, max_length=25)
  first_name = models.CharField(blank=False, max_length=25)
  last_name = models.CharField(blank=False, max_length=25)
  email = models.EmailField(blank=False, max_length=50)
  phone_number = models.CharField(blank=False, max_length=15)


class Brand(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=50)
  contacts = models.ManyToManyField(Contact)

  is_affiliated = models.BooleanField(blank=False, default=False)

