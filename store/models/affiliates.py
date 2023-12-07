from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=50)
  logo = models.ImageField(upload_to='static/images')
  
  is_affiliated = models.BooleanField(blank=False, default=False)

  def __str__(self):
    return self.name


class Contact(models.Model):
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, default=None)

  company = models.CharField(blank=False, max_length=25)
  first_name = models.CharField(blank=False, max_length=25)
  last_name = models.CharField(blank=False, max_length=25)
  email = models.EmailField(blank=False, max_length=50, unique=True)
  phone_number = models.CharField(blank=False, max_length=15, unique=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

