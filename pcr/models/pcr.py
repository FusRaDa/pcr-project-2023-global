from django.utils.timezone import now
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User

from .batch import Sample
from .inventory import Plate


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