from django.utils.timezone import now
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# **PURPOSE** #
# pcr models are exclusive to each user, 
# here users will have their own supplies 
# and the process of PCR & extraction
# **PURPOSE** #


# **START OF USER INVENTORY FUNCTIONALITY** #
# materials are exclusively meant to be for extraction
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

  class Sizes(models.TextChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')
    CUSTOM = models.IntegerField(validators=[MinValueValidator(1)])

  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)

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
    GENERAL = 'GENERAL', _('GENERAL')

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
  brand = models.CharField(blank=True, max_length=25)
  lot_number = models.CharField(blank=False, max_length=25)
  catalog_number = models.CharField(blank=False, max_length=25)
  location = models.ManyToManyField(Location)

  is_pcr_water = models.BooleanField(default=False) # if True, is used to fill well

  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.GENERAL, max_length=25)

  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=ConcentrationUnits.MILLIMOLES, max_length=25)

  last_updated = models.DateTimeField(auto_now=True)
  date_created = models.DateTimeField(default=now, editable=False)

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
# **END OF USER INVENTORY FUNCTIONALITY** #


# **START OF EXTRACTION FUNCTIONALITY** # 
class ExtractionProtocol(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # create a validation in form/views if assaylist and ExtractionProtocol type is not compatible - example: Assay (type) require RNA but batch type is DNA
  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')
    TOTAL_NUCLEIC = 'TOTAL_NUCLEIC', _('Total Nucleic') # Both DNA & RNA

  name = models.CharField(blank=False, unique=True, max_length=25)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25) # type of genetic material being extracted from samples in batch
  
  tubes = models.ManyToManyField(Tube, through='TubeExtraction')
  reagents = models.ManyToManyField(Reagent, through='ReagentExtraction')

  doc_url = models.URLField(blank=True) # store url to document there from company

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
  

class TubeExtraction(models.Model):
  tube = models.ForeignKey(Tube, on_delete=models.CASCADE)
  protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.CASCADE)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last
  amount_per_sample = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)], default=0)

  def __str__(self):
    return f'{self.tube}'
  

class ReagentExtraction(models.Model):
  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.CASCADE)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last
  amount_per_sample = models.DecimalField(decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], max_digits=12) # in microliters

  def __str__(self):
    return f'{self.reagent}'
# **END OF EXTRACTION FUNCTIONALITY** # 


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
    return f'{self.reagent}-{self.assay}'


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
# **END OF ASSAY FUNCTIONALITY** #


# **START OF SAMPLE FUNCTIONALITY** #
class Batch(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Batch refers to a list of samples that are to be extracted
  name = models.CharField(blank=False, max_length=25)
  number_of_samples = models.IntegerField(validators=[MinValueValidator(1)]) # number of samples in batch
  lab_id = models.CharField(blank=False, max_length=5) # This will be a short STRING to be shown on the plate such as ABC

  code = models.ForeignKey(AssayCode, on_delete=models.RESTRICT) # a batch can only refer to one list of assays (AssayList) - but users can individually edit samples after
  extraction_protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.RESTRICT)

  date_created = models.DateTimeField(default=now, editable=False)
  
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lab_id'], 
        name='batch_unique',
        violation_error_message = "A batch with this lab ID already exists."
      )
    ]

  @property
  def number_of_assays(self):
    return self.code.assays.count()

  @property
  def total_tests(self):
    num = self.code.assays.count()
    return self.number_of_samples * num
 
  def __str__(self):
    return f'{self.name}-{self.lab_id}'


class Sample(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  lab_id_num = models.CharField(blank=False, max_length=10) # lab id with number - auto generated by combining lab_id from Batch and adding a number to it
  sample_id = models.CharField(blank=True, max_length=25) # actual id of sample - manually generated by user by turning csv into html or copy/paste (JS)

  assays = models.ManyToManyField(Assay) # assays assigned to each sample according to AssayList assigned in Batch - users can also edit samples at this stage and add individual assays

  batch = models.ForeignKey(Batch, on_delete=models.CASCADE) # automatically assigned to newly created batch - cannot be changed

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'lab_id_num'], 
        name='user_lab_id_unique',
        violation_error_message = "A batch with this lab ID already exists.",
      )
    ]

  def __str__(self):
    return self.lab_id_num
# **END OF SAMPLE FUNCTIONALITY** #


# **START OF PROCESS (PCR) FUNCTIONALITY** #
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


class Process(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  samples = models.ManyToManyField(Sample)
  protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT) # protocol can only be deleted if no plates are using it
  plate = models.ForeignKey(Plate, on_delete=models.RESTRICT)

  date_created = models.DateTimeField(default=now, editable=False)

  def __str__(self):
    return self.samples.name


class ProcessPlate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')

  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25) # type of genetic material in plate - a plate CANNOT do both DNA & RNA

  process = models.ForeignKey(Process, on_delete=models.CASCADE)

  samples = models.ManyToManyField(Sample)
  protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT) # protocol can only be deleted if no plates are using it
  plate = models.ForeignKey(Plate, on_delete=models.RESTRICT)
# **END OF PROCESS (PCR) FUNCTIONALITY** #