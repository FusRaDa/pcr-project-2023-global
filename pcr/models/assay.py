from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.utils.timezone import now

import datetime
from django.utils import timezone

from users.models import User

from .inventory import Reagent, Location, Ladder, Dye


class Fluorescence(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=100)

  def __str__(self):
    return self.name


class Control(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Many-to-many with Assay
  name = models.CharField(blank=False, max_length=100)
  brand = models.CharField(blank=True, null=True, max_length=100)
  catalog_number = models.CharField(blank=True, null=True, max_length=100)
  lot_number = models.CharField(blank=False, max_length=100)
  amount = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  threshold = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  threshold_diff = models.IntegerField(blank=True, null=True, default=None) # amount - amount_used - threshold

  merged_lot_numbers = models.JSONField(default=list)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)
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
  
  @property
  def is_low(self):
    if self.threshold_diff and self.threshold_diff <= 0:
      return True
    return False

  def __str__(self):
    return f"{self.name}-Lot#:{self.lot_number}"


class Assay(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Methods(models.TextChoices):
    qPCR = 'qPCR', _('qPCR')
    PCR = 'PCR', _('PCR')

  # block number of instances https://stackoverflow.com/questions/44266260/django-how-can-i-limit-the-number-of-objects-that-a-user-can-create
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA') # PCR
    RNA = 'RNA', _('RNA') # RT-PCR

  name = models.CharField(blank=False, max_length=100)
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
      if reagent.reagent.pcr_reagent != Reagent.PCRReagent.WATER and reagent.reagent.pcr_reagent != Reagent.PCRReagent.MIXTURE:
        if reagent.final_concentration == None:
          return False
    return True
  
  @property
  def incomplete_reagents(self):
    for reagent in self.reagentassay_set.all():
      if reagent.reagent.pcr_reagent != Reagent.PCRReagent.WATER and reagent.reagent.pcr_reagent != Reagent.PCRReagent.MIXTURE:
        if reagent.final_concentration == None:
          return True
    return False
  
  @property
  def mm_volume(self):
    sub = self.reaction_volume - self.sample_volume
    return sub
  
  @property
  def is_alert(self):
    for reagent in self.reagents.all():
      if reagent.is_expired or (reagent.threshold_diff != None and reagent.threshold_diff <= 0):
        return True
    for control in self.controls.all():
      if control.is_expired or (control.threshold_diff != None and control.threshold_diff <= 0):
        return True
    return False

  def __str__(self):
    return self.name
  

class ControlAssay(models.Model):
  control = models.ForeignKey(Control, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  def __str__(self):
    return f'{self.control}'


class ReagentAssay(models.Model):
  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  final_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12) # in microliters
  final_concentration_unit = models.CharField(blank=True, null=True, default=None, max_length=25)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last

  @property
  def volume_per_sample(self):
    if self.reagent.pcr_reagent == Reagent.PCRReagent.WATER:

      inital_volume = self.assay.reaction_volume - self.assay.sample_volume
      sum = 0
      reagents = self.assay.reagentassay_set.all()
      for reagent in reagents:
        if reagent.reagent.pcr_reagent != Reagent.PCRReagent.WATER:
          if reagent.reagent.pcr_reagent == Reagent.PCRReagent.POLYMERASE:
            vol = reagent.final_concentration / reagent.reagent.stock_concentration
            sum += vol
          if reagent.reagent.pcr_reagent == Reagent.PCRReagent.MIXTURE:
            sum += reagent.reagent.mixture_volume_per_reaction
          else:
            dil_f = reagent.reagent.stock_concentration / reagent.final_concentration
            vol = reagent.assay.reaction_volume / dil_f
            sum += vol
      
      volume = Decimal("{:.2f}".format(inital_volume - sum))
      return volume
    
    if self.reagent.pcr_reagent == Reagent.PCRReagent.POLYMERASE:
      volume = self.final_concentration / self.reagent.stock_concentration 
      return volume
    
    if self.reagent.pcr_reagent == Reagent.PCRReagent.MIXTURE:
      volume = reagent.reagent.mixture_volume_per_reaction
      return volume

    df = self.reagent.stock_concentration / self.final_concentration 
    volume = Decimal("{:.2f}".format(self.assay.reaction_volume / df))

    return volume
  
  @property
  def dilution_factor(self):
    if self.reagent.pcr_reagent == Reagent.PCRReagent.WATER or self.reagent.pcr_reagent == Reagent.PCRReagent.POLYMERASE or self.reagent.pcr_reagent == Reagent.PCRReagent.MIXTURE:
      return None
    df = Decimal("{:.2f}".format(self.reagent.stock_concentration / self.final_concentration))
    return df
  
  def __str__(self):
    return f'{self.reagent}'


class AssayCode(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # AssayList is used to bundle assays together making creating a batch easier rather then selecting all assays
  name = models.CharField(blank=False, max_length=100)
  assays = models.ManyToManyField(Assay)

  def __str__(self):
    return self.name