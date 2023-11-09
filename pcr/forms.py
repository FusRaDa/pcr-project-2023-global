from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

# INVENTORY #
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
# INVENTORY #


# EXTRACTION #
class ExtractionProtocolForm(ModelForm):
  class Meta:
    model = ExtractionProtocol
    exclude = ['user']


class TubeExtractionForm(ModelForm):
  class Meta:
    model = TubeExtraction
    exclude = ['tube', 'protocol']


class ReageExtractionForm(ModelForm):
  class Meta:
    model = ReagentExtraction
    exclude = ['reagent', 'protocol']
# EXTRACTION #


# ASSAY #
class FlourescenceForm(ModelForm):
  class Meta:
    model = Flourescence
    exclude = ['user']


class ControlForm(ModelForm):
  class Meta:
    model = Control
    exclude = ['user']


class AssayForm(ModelForm):
  class Meta:
    model = Assay
    exclude = ['user']


class ReagentAssayForm(ModelForm):
  class Meta:
    model = ReagentAssay
    exclude = ['reagent', 'assay']


class AssayCodeForm(ModelForm):
  class Meta:
    model = AssayCode
    exclude = ['user']
# ASSAY #


# SAMPLE #
class BatchForm(ModelForm):
  class Meta:
    model = Batch
    exclude = ['user', 'date_performed']


class SampleForm(ModelForm):
  class Meta:
    model = Sample
    exclude = ['user', 'batch']
# SAMPLE #


# PROCESS #





