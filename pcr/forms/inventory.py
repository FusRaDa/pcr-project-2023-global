from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Plate, Tube, Reagent, Location


class LocationForm(ModelForm):
  class Meta:
    model = Location
    exclude = ['user']


class PlateForm(ModelForm):
  class Meta:
    model = Plate
    exclude = ['user', 'last_updated']


class TubeForm(ModelForm):
  class Meta:
    model = Tube
    exclude = ['user', 'last_updated']


class ReagentForm(ModelForm):
  class Meta:
    model = Reagent
    exclude = ['user', 'last_updated']