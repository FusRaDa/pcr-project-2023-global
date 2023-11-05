from django.utils.timezone import now
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



# Create your models here.

# **START OF REAGENT FUNCTIONALITY** #
class Reagent(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # exclude Template DNA - in the future have a DB where users can add reagents to their accounts
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
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)
  storage_location = models.CharField(max_length=25)
  last_updated = models.DateTimeField(auto_now=True)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=ConcentrationUnits.MILLIMOLES, max_length=25)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lot_number', 'catalog_number'], 
        name='reagent_unique',
        violation_error_message = "A reagent with the same lot and catalog number already exists."
      )
    ]
    
    
  def __str__(self):
    return self.name
# **END OF REAGENT FUNCTIONALITY** #
  
  
# **START OF ASSAY FUNCTIONALITY** #
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

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lot_number'], 
        name='control_unique',
        violation_error_message = "A control with this lot number already exists."
      )
    ]

  def __str__(self):
    return self.name
  

class Assay(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # block number of instances https://stackoverflow.com/questions/44266260/django-how-can-i-limit-the-number-of-objects-that-a-user-can-create
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA') # PCR
    RNA = 'RNA', _('RNA') # RT-PCR

  name = models.CharField(blank=False, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25)

  fluorescence = models.ManyToManyField(Flourescence)
  controls = models.ManyToManyField(Control, through='ControlOrder')
  reagents = models.ManyToManyField(Reagent, through='ReagentOrder')

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
  

class AssayList(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # AssayList is used to bundle assays together making creating a batch easier rather then selecting all assays
  name = models.CharField(blank=False, max_length=25)
  assays = models.ManyToManyField(Assay)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='assay_list_unique',
        violation_error_message = "An assay list/group with this name already exists."
      )
    ]

  def __str__(self):
    return self.name
# **END OF ASSAY FUNCTIONALITY** #
  

# **START OF ORDER FUNCTIONALITY** #
# THROUGH Table in relation to control -> assay AND reagent -> assay
class ControlOrder(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # 1-lowest priority > highest priority, 0 will be last
  control = models.ForeignKey(Control, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.user}-{self.control}-{self.order}'
  

class ReagentOrder(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # 1-lowest priority > highest priority, 0 will be last
  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  assay = models.ForeignKey(Assay, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.user}-{self.reagent}-{self.order}'
# **END OF ORDER FUNCTIONALITY** #


# **START OF SAMPLE FUNCTIONALITY** #
class ExtractionProtocol(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # create a validation in form/views if assaylist and ExtractionProtocol type is not compatible - example: Assay (type) require RNA but batch type is DNA
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')
    TOTAL_NUCLEIC = 'TOTAL_NUCLEIC', _('Total Nucleic') # Both DNA & RNA

  name = models.CharField(blank=False, unique=True, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25) # type of genetic material being extracted from samples in batch

  reagents = models.ManyToManyField(Reagent)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='extraction_protocol_unique',
        violation_error_message = "An extraction protocol with this name already exists."
      )
    ]

  def __str__(self):
    return self.name


class Batch(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Batch refers to a list of samples that are to be extracted
  name = models.CharField(blank=False, max_length=25)
  number_of_samples = models.IntegerField(validators=[MinValueValidator(1)]) # number of samples in batch
  lab_id = models.CharField(blank=False, max_length=5) # This will be a short STRING to be shown on the plate such as ABC
  date_created = models.DateTimeField(default=now, editable=False)

  assay_list = models.ForeignKey(AssayList, on_delete=models.RESTRICT) # a batch can only refer to one list of assays (AssayList) - user can edit samples individually after batch is created
  extraction_protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.RESTRICT)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lab_id'], 
        name='batch_unique',
        violation_error_message = "A batch with this lab ID already exists."
      )
    ]

  def __str__(self):
    return f'{self.name}-{self.lab_id}'

  
class Sample(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  lab_id_num = models.CharField(blank=False, max_length=10) # lab id with number - auto generated by combining lab_id from Batch and adding a number to it
  sample_id = models.CharField(blank=True, max_length=25) # actual id of sample - manually generated by user by turning csv into html or copy/paste (JS)

  assay_name = models.CharField(blank=True, max_length=25)
  assays = models.ManyToManyField(Assay) # assays assigned to each sample according to AssayList assigned in Batch - users can also edit samples at this stage and add individual assays

  batch = models.ForeignKey(Batch, on_delete=models.CASCADE) # automatically assigned to newly created batch - cannot be changed

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lab_id_num'], 
        name='sample_unique',
        violation_error_message = "A batch with this lab ID already exists."
      )
    ]

  def __str__(self):
    return self.lab_id_num
# **END OF SAMPLE FUNCTIONALITY** #


# **START OF PLATE FUNCTIONALITY** #
class SampleList(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)
  samples = models.ManyToManyField(Sample) # user can select samples individually or by batch

  def __str__(self):
    return self.name
  

class ThermalCyclerProtocol(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=25)
  denature_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  denature_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  anneal_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  anneal_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  extension_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  extension_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  number_of_cycles = models.IntegerField(validators=[MinValueValidator(0)])

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'name'], 
        name='thermal_cycler_protocol_unique',
        violation_error_message = "A protocol with this name already exists."
      )
    ]

  def __str__(self):
    return self.name
  
  
class Plate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')

  class Sizes(models.TextChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')
    CUSTOM = models.IntegerField(validators=[MinValueValidator(1)])

  name = models.CharField(blank=False, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25) # type of genetic material in plate - a plate CANNOT do both DNA & RNA
  plate_size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT, blank=False) # protocol can only be deleted if no plates are using it

  samples = models.ManyToManyField(SampleList)

  def __str__(self):
    return self.name
  # **END OF PLATE FUNCTIONALITY** #


  
