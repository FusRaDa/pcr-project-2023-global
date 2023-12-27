from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User
from .inventory import Reagent, Tube


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
  amount_per_sample = models.IntegerField(validators=[MinValueValidator(1)], default=1)

  def __str__(self):
    return f'{self.tube}'
  

class ReagentExtraction(models.Model):
  reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
  protocol = models.ForeignKey(ExtractionProtocol, on_delete=models.CASCADE)

  order = models.IntegerField(validators=[MinValueValidator(0)], default=0) # users can decide what order reagents will be que's/displayed: 1-lowest priority > highest priority, 0 will be last
  amount_per_sample = models.DecimalField(decimal_places=2, validators=[MinValueValidator(1)], max_digits=12, default=1) # in microliters

  def __str__(self):
    return f'{self.reagent}'