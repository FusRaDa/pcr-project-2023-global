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

  class Sizes(models.IntegerChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  
  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)

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
  exp_date = models.DateField(blank=True, null=True, default=None)

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

  class VolumeUnits(models.TextChoices):
    LITER = 'L', _('L')
    MILLILITER = 'mL', _('mL')
    MICROLITER = '\u00B5L', _('\u00B5L')

  class ConcentrationUnits(models.TextChoices):
    MOLES = 'M', _('M')
    MILLIMOLES = 'mM', _('mM')
    MICROMOLES = '\u00B5M', _('\u00B5M')
    NANOMOLES = 'nM', _('nM')
    UNITS = 'U/\u00B5L', _('U/\u00B5L')
    X = 'X', _('X')

  class PCRReagent(models.TextChoices):
    GENERAL = 'GENERAL', _('GENERAL')
    POLYMERASE = 'POLYMERASE', _('POLYMERASE')
    WATER = 'WATER', _('WATER')

  class IsPolymerase(models.TextChoices):
    TRUE = 'TRUE', _('TRUE')
    FALSE = 'FALSE', _('FALSE')

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)
  location = models.ManyToManyField(Location)

  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.PCR, max_length=25)
  pcr_reagent = models.CharField(choices=PCRReagent.choices, blank=True, null=True, default=None, max_length=25) # determine calculations for type of pcr reagent
 
  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=None, max_length=25)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)

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