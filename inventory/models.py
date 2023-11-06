from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# **PURPOSE** #
# inventory models serve as a store 
# for users to add to their accounts, 
# such as Plates, Reagents, Solutions, etc...
# **PURPOSE** #

# **START OF STORE INVENTORY FEATURE** #
# Product is what will be displayed on web page
class Product(models.Model):
  name = models.CharField(blank=False, max_length=25)

  def __str__(self):
    return self.name
  

class StorePlate(models.Model):
  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  class Sizes(models.TextChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')
    CUSTOM = models.IntegerField(validators=[MinValueValidator(1)])

  plate_size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)

  number = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['lot_number', 'catalog_number'], 
        name='store_plate_unique',
        violation_error_message = "Tubes with the same lot and catalog number already exists."
      )
    ]

  def __str__(self):
    return self.name
  

class StoreTube(models.Model):

  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  number = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  number_per_sample = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['lot_number', 'catalog_number'], 
        name='store_tube_unique',
        violation_error_message = "Tubes with the same lot and catalog number already exists."
      )
    ]

  def __str__(self):
    return self.name


class StoreSolution(models.Model):
  name = models.CharField(blank=False, max_length=25)
  brand = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  volume_per_sample = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['lot_number', 'catalog_number'], 
        name='store_solution_unique',
        violation_error_message = "Solutions with the same lot and catalog number already exists."
      )
    ]

  def __str__(self):
    return self.name
  

class StoreReagent(models.Model):
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
  brand = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)

  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=ConcentrationUnits.MILLIMOLES, max_length=25)

  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['lot_number', 'catalog_number'], 
        name='store_reagent_unique',
        violation_error_message = "Reagents with the same lot and catalog number already exists."
      )
    ]
    
  def __str__(self):
    return self.name
# **END OF STORE INVENTORY FEATURE** #
