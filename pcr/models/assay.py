from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

import datetime
from django.utils import timezone

from users.models import User

from .inventory import Reagent, Location, Ladder, Dye


class Fluorescence(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=25)

  def __str__(self):
    return self.name


class Control(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  amount = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  exp_date = models.DateField(blank=True, null=True, default=None)

  location = models.ManyToManyField(Location)

  @property
  def is_expired(self):
    if self.exp_date != None and (self.exp_date <= timezone.now().date()):
      return True
    return False
    
  @property
  def month_exp(self):
    if self.exp_date != None and (self.exp_date > timezone.now().date()) and (self.exp_date - timezone.now().date() <= datetime.timedelta(days=30)):
      return True
    return False

  def __str__(self):
    return self.name


class Assay(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Methods(models.TextChoices):
    qPCR = 'qPCR', _('qPCR')
    PCR = 'PCR', _('PCR')

  # block number of instances https://stackoverflow.com/questions/44266260/django-how-can-i-limit-the-number-of-objects-that-a-user-can-create
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA') # PCR
    RNA = 'RNA', _('RNA') # RT-PCR

  name = models.CharField(blank=False, max_length=25)
  method = models.CharField(choices=Methods.choices, blank=False, default=Methods.PCR, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25)

  sample_volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  reaction_volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  ladder = models.ForeignKey(Ladder, blank=True, null=True, default=None, on_delete=models.PROTECT)
  ladder_volume_per_gel = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12, default=0) # in microliters

  dye = models.ForeignKey(Dye, blank=True, null=True, default=None, on_delete=models.PROTECT)
  dye_volume_per_well = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12, default=0) # in microliters
  dye_in_ladder = models.BooleanField(default=False)

  multiplicates = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
  
  fluorescence = models.ManyToManyField(Fluorescence)
  controls = models.ManyToManyField(Control, through='ControlAssay')
  reagents = models.ManyToManyField(Reagent, through='ReagentAssay')

  @property
  def is_complete(self):
    if self.controls.count() < 1 or self.reagents.count() < 1:
      return False
    
    for reagent in self.reagentassay_set.all():
      if reagent.reagent.pcr_reagent != Reagent.PCRReagent.WATER and reagent.final_concentration == None:
        return False
    
    return True
  
  @property
  def mm_volume(self):
    sub = self.reaction_volume - self.sample_volume
    return sub

  def __str__(self):
    return self.name
  

class ControlAssay(models.Model):
  control = models.ForeignKey(Control, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  def __str__(self):
    return f'{self.control}'


class ReagentAssay(models.Model):

  class ConcentrationUnits(models.TextChoices):
    MOLES = 'MOLES', _('M')
    MILLIMOLES = 'MILLIMOLES', _('mM')
    MICROMOLES = 'MICROMOLES', _('\u00B5M')
    NANOMOLES = 'NANOMOLES', _('nM')
    UNITS = 'UNITS', _('U/\u00B5L')
    X = 'X', _('X')

  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  final_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  final_concentration_unit = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=None, max_length=25)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last

  @property
  def volume_per_sample(self):
    if self.reagent.pcr_reagent == Reagent.PCRReagent.WATER:

      inital_volume = self.assay.reaction_volume - self.assay.sample_volume
      sum = 0
      reagents = self.assay.reagentassay_set.all()
      for reagent in reagents:
        if reagent.reagent.pcr_reagent != Reagent.PCRReagent.WATER:
          dil_f = reagent.reagent.stock_concentration / reagent.final_concentration
          vol = reagent.assay.reaction_volume / dil_f
          sum += vol
      
      volume = Decimal("{:.2f}".format(inital_volume - sum))
      return volume
    
    df = self.reagent.stock_concentration / self.final_concentration 
    volume = Decimal("{:.2f}".format(self.assay.reaction_volume / df))

    return volume
  
  @property
  def dilution_factor(self):
    if self.reagent.pcr_reagent == Reagent.PCRReagent.WATER:
      return None
    df = Decimal("{:.2f}".format(self.reagent.stock_concentration / self.final_concentration))
    return df
  
  def __str__(self):
    return f'{self.reagent}'


class AssayCode(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # AssayList is used to bundle assays together making creating a batch easier rather then selecting all assays
  name = models.CharField(blank=False, max_length=25)
  assays = models.ManyToManyField(Assay)

  def __str__(self):
    return self.name