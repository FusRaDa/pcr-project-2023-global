from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Brand(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=50)
  logo = models.ImageField(null=True, blank=True, upload_to='main/static/brands')
  is_affiliated = models.BooleanField(blank=False, default=False)

  @property
  def affiliate(self):
    if self.is_affiliated:
      return "✔"
    else:
      return ""
  
  @property
  def abs_url(self):
    try:
      url = self.logo.url
      abs = url.replace("/main", "")
      return abs
    except ValueError:
      return '/static/brands/default-brand.png'

  def __str__(self):
    return self.name


class Contact(models.Model):
  brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True, default=None)

  company = models.CharField(blank=False, max_length=25)
  first_name = models.CharField(blank=False, max_length=25)
  last_name = models.CharField(blank=False, max_length=25)
  email = models.EmailField(blank=False, max_length=50, unique=True)
  phone_number = PhoneNumberField(blank=False, max_length=15, unique=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"