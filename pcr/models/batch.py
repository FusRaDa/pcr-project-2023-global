from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

from .assay import AssayCode, Assay
from .extraction import ExtractionProtocol

# Batches can only be created and deleted. If changes such as lab ID or number of samples must be made to a batch it must be deleted and created again.
# A batch is a set of samples with the extraction protocol where sample assays can be individually added/removed
class Batch(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Batch refers to a list of samples that are to be extracted
  name = models.CharField(blank=False, max_length=25)
  lab_id = models.CharField(blank=False, max_length=3) # This will be a short STRING to be shown on the plate such as ABC

  code = models.ForeignKey(AssayCode, on_delete=models.RESTRICT) # a batch can only refer to one list of assays (AssayList) - but users can individually edit samples after
  extraction_protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.RESTRICT)

  is_extracted = models.BooleanField(default=False) # Once set to true, batch and samples can no longer be edited and files for extraction are generated.

  date_created = models.DateTimeField(default=now, editable=False)

  negative_control = models.BooleanField(default=True)

  @property
  def contains_anomaly(self):
    anomaly_detected = False
    assays_in_code = self.code.assays.all()
    for sample in self.sample_set.all():
      if set(sample.assays.all()) != set(assays_in_code):
        anomaly_detected = True
        break
    return anomaly_detected
  
  @property
  def number_of_anomalies(self):
    anomalies = 0
    assays_in_code = self.code.assays.all()
    for sample in self.sample_set.all():
      if set(sample.assays.all()) != set(assays_in_code):
        anomalies += 1
    return anomalies
     
  @property
  def number_of_assays(self):
    if self.contains_anomaly:
      return f"{self.code.assays.count()} ⚠"
    else:
      return self.code.assays.count()

  @property
  def number_of_samples(self):
    if self.negative_control:
      if self.contains_anomaly:
        return f"{self.sample_set.count() - 1} + 1(NC) ⚠"
      else:
        return f"{self.sample_set.count() - 1} + 1(NC)"
    else:
      if self.contains_anomaly:
        return f"{self.sample_set.count()} ⚠"
      else:
        return f"{self.sample_set.count()}"
  
  @property
  def total_samples(self):
    return self.sample_set.count() 
  
  @property
  def total_tests(self):
    total_tests = 0
    for sample in self.sample_set.all():
      total_tests += sample.assays.count()
    
    if self.contains_anomaly:
      return f"{total_tests} ⚠"
    else:
      return total_tests

  def __str__(self):
    return f'{self.name}-{self.lab_id}'


class Sample(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  lab_id_num = models.CharField(blank=False, max_length=10) # lab id with number - auto generated by combining lab_id from Batch and adding a number to it
  sample_id = models.CharField(blank=True, max_length=25) # actual id of sample - manually generated by user by turning csv into html or copy/paste (JS)

  assays = models.ManyToManyField(Assay) # assays assigned to each sample according to AssayList assigned in Batch - users can also edit samples at this stage and add individual assays

  batch = models.ForeignKey(Batch, on_delete=models.CASCADE) # automatically assigned to newly created batch - cannot be changed

  @property
  def is_anomaly(self):
    if set(self.assays.all()) != set(self.batch.code.assays.all()):
      return True
    else:
      return False

  def __str__(self):
    return self.lab_id_num