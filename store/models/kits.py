from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from ..models.items import StorePlate, StoreTube, StoreReagent


class Kit(models.Model):
  name = models.CharField(blank=False, max_length=50)
  catalog_number = models.CharField(blank=False, max_length=25)
  price = models.DecimalField(blank=False, decimal_places=2, max_digits=7)

  tubes = models.ManyToManyField(StoreTube)
  plates = models.ManyToManyField(StorePlate)
  reagents = models.ManyToManyField(StoreReagent)
  