from django.contrib import admin
from .models import *

# Register your models here.

pcr_models = [
  Reagent, Flourescence, Control, 
  Assay, AssayCode, ExtractionProtocol, 
  Batch, Sample, ThermalCyclerProtocol, 
  Plate, ReagentAssay, Process, 
  ProcessPlate, Tube, Location,
  ReagentExtraction, TubeExtraction,
]

admin.site.register(pcr_models)
