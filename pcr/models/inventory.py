from django.utils.timezone import now
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

import datetime
from django.utils import timezone

from users.models import User


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
  

class Ladder(models.Model):
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

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    else:
      return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    else:
      return False

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
  
  class Types(models.TextChoices):
    PCR = 'PCR', _('PCR')
    qPCR = 'qPCR', _('qPCR')

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.PCR, max_length=25)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  
  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    else:
      return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    else:
      return False

  def __str__(self):
    return f"{self.name}-Lot#:{self.lot_number}"
  

class Gel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  location = models.ManyToManyField(Location)

  class Sizes(models.IntegerChoices):
    TWELVE = 12, _('12')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.TWENTY_FOUR, blank=False)

  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  
  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
  exp_date = models.DateField(blank=True, null=True, default=None)

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    else:
      return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    else:
      return False

  def __str__(self):
    return f"{self.name}-Lot#:{self.lot_number}"


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

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    else:
      return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    else:
      return False

  def __str__(self):
    return f"{self.name}-Lot#:{self.lot_number}"


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
    POLYMERASE = 'POLYMERASE', _('POLYMERASE') #used as units/micro-liter
    WATER = 'WATER', _('WATER')

  name = models.CharField(blank=False, max_length=50)
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

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    else:
      return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    else:
      return False

  @property
  def volume_in_microliters(self):
    if self.unit_volume == Reagent.VolumeUnits.LITER:
      return self.volume * 1000000
    if self.unit_volume == Reagent.VolumeUnits.MILLILITER:
      return self.volume * 1000
    if self.unit_volume == Reagent.VolumeUnits.MICROLITER:
      return self.volume

  def __str__(self):
    return f"{self.name}-Lot#:{self.lot_number}"