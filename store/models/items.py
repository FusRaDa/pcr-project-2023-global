from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from ..models.affiliates import Brand


class Tag(models.Model):
  name = models.CharField(blank=False, max_length=50, unique=True)

  def __str__(self):
    return self.name


class Kit(models.Model):
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

  image = models.ImageField(null=True, blank=True)

  name = models.CharField(blank=False, max_length=50)
  catalog_number = models.CharField(blank=False, max_length=25, unique=True)
  price = models.DecimalField(blank=False, decimal_places=2, max_digits=7) #USD

  affiliate_link = models.URLField(max_length=200, blank=True, null=True)

  tags = models.ManyToManyField(Tag)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['brand', 'catalog_number'], 
        name='kit_unique',
        violation_error_message = "A kit with the same brand and catalog number already exists.",
      )
    ]

  def __str__(self):
    return f"{self.name}-{self.catalog_number}"


class StorePlate(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
  
  class Sizes(models.IntegerChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')

  name = models.CharField(blank=False, max_length=25, default="PLATE")

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  def __str__(self):
    return self.name


class StoreTube(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25, default="TUBE")
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  def __str__(self):
    return self.name


# reagents are exclusively meant to be for PCR
class StoreReagent(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

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

  name = models.CharField(blank=False, max_length=50, default="REAGENT")
  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.PCR, max_length=25)
  pcr_reagent = models.CharField(choices=PCRReagent.choices, blank=True, null=True, default=None, max_length=25) # determine calculations for type of pcr reagent
 
  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12, default=1)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=None, max_length=25)

  def __str__(self):
    return self.name
  
