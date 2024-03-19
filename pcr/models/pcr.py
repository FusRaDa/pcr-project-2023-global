from django.utils.timezone import now
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User

from .batch import Sample, Batch
from .inventory import Plate, Gel
from .assay import Assay


class ThermalCyclerProtocol(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Types(models.TextChoices):
    DNA = 'DNA', _('DNA')
    RNA = 'RNA', _('RNA')

  type = models.CharField(choices=Types.choices, blank=False, default=Types.DNA, max_length=25) # genetic material in thermal cycler/plate

  name = models.CharField(blank=False, max_length=100)
  denature_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  denature_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  anneal_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  anneal_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  extension_temp = models.DecimalField(decimal_places=2, max_digits=12) # Celsius
  extension_duration = models.IntegerField(validators=[MinValueValidator(0)]) # seconds
  number_of_cycles = models.IntegerField(validators=[MinValueValidator(0)])

  def __str__(self):
    return self.name


class Process(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  name = models.CharField(blank=True, null=True, default=None, max_length=100)

  class LoadingMethod(models.TextChoices):
    ORGANIZED = 'ORGANIZED', _('Organized')
    COMPRESSED = 'COMPRESSED', _('Compressed')

  loading_method_dna = models.CharField(choices=LoadingMethod.choices, blank=False, default=LoadingMethod.ORGANIZED, max_length=25)
  loading_method_rna = models.CharField(choices=LoadingMethod.choices, blank=False, default=LoadingMethod.ORGANIZED, max_length=25)
  loading_method_qdna = models.CharField(choices=LoadingMethod.choices, blank=False, default=LoadingMethod.ORGANIZED, max_length=25)
  loading_method_qrna = models.CharField(choices=LoadingMethod.choices, blank=False, default=LoadingMethod.ORGANIZED, max_length=25)

  is_plus_one_well = models.BooleanField(default=True)

  pcr_dna_protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT, related_name='pcr_dna', blank=True, null=True, default=None)
  pcr_rna_protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT, related_name='pcr_rna', blank=True, null=True, default=None)

  qpcr_dna_protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT, related_name='qpcr_dna', blank=True, null=True, default=None)
  qpcr_rna_protocol = models.ForeignKey(ThermalCyclerProtocol, on_delete=models.RESTRICT, related_name='qpcr_rna', blank=True, null=True, default=None)

  qpcr_plate = models.ManyToManyField(Plate, related_name='qpcr_plate')
  pcr_plate = models.ManyToManyField(Plate, related_name='pcr_plate')

  gel = models.ManyToManyField(Gel)
  samples = models.ManyToManyField(Sample)

  min_samples_per_plate_dna_qpcr = models.IntegerField(default=0, validators=[MinValueValidator(0)])
  min_samples_per_plate_rna_qpcr = models.IntegerField(default=0, validators=[MinValueValidator(0)])

  min_samples_per_plate_dna_pcr = models.IntegerField(default=0, validators=[MinValueValidator(0)])
  min_samples_per_plate_rna_pcr = models.IntegerField(default=0, validators=[MinValueValidator(0)])

  min_samples_per_gel = models.IntegerField(default=0, validators=[MinValueValidator(0)])

  date_processed = models.DateTimeField(blank=True, null=True, editable=False, default=None)

  pcr_dna_json = models.JSONField(blank=True, null=True, default=None)
  pcr_rna_json = models.JSONField(blank=True, null=True, default=None)

  pcr_gels_json = models.JSONField(blank=True, null=True, default=None)

  qpcr_dna_json = models.JSONField(blank=True, null=True, default=None)
  qpcr_rna_json = models.JSONField(blank=True, null=True, default=None)

  plates_for_qpcr = models.JSONField(blank=True, null=True, default=None)
  plates_for_pcr = models.JSONField(blank=True, null=True, default=None)
  gels = models.JSONField(blank=True, null=True, default=None)
  reagent_usage = models.JSONField(blank=True, null=True, default=None)
  control_usage = models.JSONField(blank=True, null=True, default=None)

  batches = models.ManyToManyField(Batch)

  is_processed = models.BooleanField(default=False)

  @property
  def lab_ids(self):
    lab_ids_array = []
    for batch in self.batches.all():
      lab_ids_array.append(batch.lab_id)
    return lab_ids_array
  
  @property
  def panels(self):
    panels_array = []
    for batch in self.batches.all():
      panels_array.append(batch.code)
    panels = list(set(panels_array))
    return panels
  
  @property
  def selected_panels(self):
    arr = []
    for sample in self.samples.all():
      arr.append(sample.batch)
    batches = list(set(arr))

    panels_array = []
    for batch in batches:
      panels_array.append(batch.code)
    panels = list(set(panels_array))
    return panels
  
  @property
  def is_dna_pcr(self):
    for panel in self.selected_panels:
      for assay in panel.assays.all():
        if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.PCR:
          return True
    return False
  
  @property
  def is_rna_pcr(self):
    for panel in self.selected_panels:
      for assay in panel.assays.all():
        if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.PCR:
          return True
    return False
  
  @property
  def is_dna_qpcr(self):
    for panel in self.selected_panels:
      for assay in panel.assays.all():
        if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.qPCR:
          return True
    return False
  
  @property
  def is_rna_qpcr(self):
    for panel in self.selected_panels:
      for assay in panel.assays.all():
        if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.qPCR:
          return True
    return False

  def __str__(self):
    return f"Process by {self.user}"