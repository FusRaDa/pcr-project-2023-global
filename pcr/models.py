from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


# Create your models here.

class Reagent(models.Model):
  # exclude Template DNA

  class VolumeUnits(models.TextChoices):
    MILLILITER = 'MILLILITER', _('mL')
    MICROLITER = 'MICROLITER', _('\u00B5L')

  class ConcentrationUnits(models.TextChoices):
    NOT_APPLICABLE = 'NOT_APPLICABLE', _('NOT_APPLICABLE')
    MILLIMOLES = 'MILLIMOLES', _('mM')
    MICROMOLES = 'MICROMOLES', _('\u00B5M')
    NANOMOLES = 'NANOMOLES', _('nM')
    UNITS = 'UNITS', _('U/\u00B5L')

  name = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)
  storage_location = models.CharField(max_length=25)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=False, default=ConcentrationUnits.MILLIMOLES, max_length=25)

  class Meta:
    constraints = [
      UniqueConstraint(
        Lower('lot_number'),
        Lower('catalog_number'),
        name='lot_catalog_number_unique',
        violation_error_message = "A reagent with the same lot and catalog number already exists."
      )
    ]
  
  def __str__(self):
    return self.name


# order displayed will be a integer system that will determine the order these models will be shown when que'd
class Flourescence(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=25)
  order_displayed = models.IntegerField(validators=[MinValueValidator(1)])

  def __str__(self):
    return self.name


class Control(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=25)
  order_displayed = models.IntegerField(validators=[MinValueValidator(1)])

  def __str__(self):
    return self.name


class Assay(models.Model):

  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')
    TOTAL_NUCLEIC = 'TOTAL_NUCLEIC', _('Total Nucleic')

  name = models.CharField(blank=False, unique=True, max_length=25)
  sample_type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25)

  controls = models.ManyToManyField(Control)
  fluorescence = models.ManyToManyField(Flourescence)
  reagents = models.ManyToManyField(Reagent)

  def __str__(self):
    return self.name


class AssayList(models.Model):
  name = models.CharField(unique=True, blank=False, max_length=25)
  assays = models.ManyToManyField(Assay)

  def __str__(self):
    return self.name


class ThermalCyclerProtocol(models.Model):
  name = models.CharField(blank=False, max_length=25)
  denature_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  denature_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  anneal_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  anneal_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  extension_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  extension_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  number_of_cycles = models.IntegerField(validators=[MinValueValidator(0)])

  def __str__(self):
    return self.name