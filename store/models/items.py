from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class StorePlate(models.Model):
  name = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

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

  def __str__(self):
    return self.name


class StoreTube(models.Model):
  name = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
 
  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)

  def __str__(self):
    return self.name


# reagents are exclusively meant to be for PCR
class StoreReagent(models.Model):

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
    POLYMERASE = 'POLYMERASE', _('POLYMERASE') #used as units/micro-liter
    WATER = 'WATER', _('WATER')

  name = models.CharField(blank=False, max_length=50)
  catalog_number = models.CharField(blank=False, max_length=25)

  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.PCR, max_length=25)
  pcr_reagent = models.CharField(choices=PCRReagent.choices, blank=True, null=True, default=None, max_length=25) # determine calculations for type of pcr reagent
 
  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=None, max_length=25)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)
    
  def __str__(self):
    return f"{self.name}-{self.catalog_number}"
  
