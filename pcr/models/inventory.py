from django.utils.timezone import now
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Location(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='location_unique',
        violation_error_message = "A location with the same name already exists.",
      )
    ]
  
  def __str__(self):
    return self.name


class Plate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  location = models.ManyToManyField(Location)

  class Sizes(models.TextChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')
    CUSTOM = models.IntegerField(validators=[MinValueValidator(1)])

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lot_number', 'catalog_number'], 
        name='plate_unique',
        violation_error_message = "Tubes with the same lot and catalog number already exists."
      )
    ]

  def __str__(self):
    return self.name


class Tube(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  location = models.ManyToManyField(Location)

  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
 
  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lot_number', 'catalog_number'], 
        name='tube_unique',
        violation_error_message = "Tubes with the same lot and catalog number already exists."
      )
    ]

  def __str__(self):
    return self.name


# reagents are exclusively meant to be for PCR
class Reagent(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Usages(models.TextChoices):
    EXTRACTION = 'EXTRACTION', _('EXTRACTION')
    PCR = 'PCR', _('PCR')
    GENERAL = 'GENERAL', _('GENERAL')

  class VolumeUnits(models.TextChoices):
    LITER = 'LITER', _('L')
    MILLILITER = 'MILLILITER', _('mL')
    MICROLITER = 'MICROLITER', _('\u00B5L')

  class ConcentrationUnits(models.TextChoices):
    NOT_APPLICABLE = 'NOT_APPLICABLE', _('NOT_APPLICABLE')
    MOLES = 'MOLES', _('M')
    MILLIMOLES = 'MILLIMOLES', _('mM')
    MICROMOLES = 'MICROMOLES', _('\u00B5M')
    NANOMOLES = 'NANOMOLES', _('nM')
    UNITS = 'UNITS', _('U/\u00B5L')
    X = 'X', _('X')

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)
  location = models.ManyToManyField(Location)

  is_pcr_water = models.BooleanField(default=False) # if True, is used to fill well

  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.GENERAL, max_length=25)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=ConcentrationUnits.MILLIMOLES, max_length=25)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lot_number', 'catalog_number'], 
        name='reagent_unique',
        violation_error_message = "Reagents with the same lot and catalog number already exists."
      )
    ]
    
  def __str__(self):
    return self.name