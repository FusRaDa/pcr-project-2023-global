from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .inventory import Reagent


class Flourescence(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=25)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='flourescence_unique',
        violation_error_message = "Flourescense with this name already exists."
      )
    ]

  def __str__(self):
    return self.name


class Control(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  amount = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  def __str__(self):
    return self.name


class Assay(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Method(models.TextChoices):
    qPCR = 'qPCR', _('qPCR')
    PCR = 'PCR', _('PCR')

  # block number of instances https://stackoverflow.com/questions/44266260/django-how-can-i-limit-the-number-of-objects-that-a-user-can-create
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA') # PCR
    RNA = 'RNA', _('RNA') # RT-PCR

  name = models.CharField(blank=False, max_length=25)
  method = models.CharField(choices=Method.choices, blank=False, default=Method.qPCR, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25)

  sample_volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  reaction_volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  
  fluorescence = models.ManyToManyField(Flourescence)
  controls = models.ManyToManyField(Control)
  reagents = models.ManyToManyField(Reagent, through='ReagentAssay')

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='assay_unique',
        violation_error_message = "An assay with this name already exists."
      )
    ]

  def __str__(self):
    return self.name


class ReagentAssay(models.Model):

  class ConcentrationUnits(models.TextChoices):
    NOT_APPLICABLE = 'NOT_APPLICABLE', _('NOT_APPLICABLE')
    MOLES = 'MOLES', _('M')
    MILLIMOLES = 'MILLIMOLES', _('mM')
    MICROMOLES = 'MICROMOLES', _('\u00B5M')
    NANOMOLES = 'NANOMOLES', _('nM')
    UNITS = 'UNITS', _('U/\u00B5L')
    X = 'X', _('X')

  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  final_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  final_concentration_unit = models.CharField(choices=ConcentrationUnits.choices, default=ConcentrationUnits.MICROMOLES, max_length=25)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last

  def __str__(self):
    return f'{self.reagent}'


class AssayCode(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # AssayList is used to bundle assays together making creating a batch easier rather then selecting all assays
  name = models.CharField(blank=False, max_length=25)
  assays = models.ManyToManyField(Assay)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='assay_code_unique',
        violation_error_message = "An assay list/group with this name already exists."
      )
    ]

  def __str__(self):
    return self.name