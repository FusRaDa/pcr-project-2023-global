from django.contrib import admin
from .models import *

# Register your models here.

pcr_models = [
  Reagent, Flourescence, Control, 
  Assay, AssayList, ExtractionProtocol, 
  Batch, Sample, SampleList, 
  ThermalCyclerProtocol, Plate, ReagentOrder,
  ControlOrder,
]

admin.site.register(pcr_models)
