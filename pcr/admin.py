from django.contrib import admin
from .models import *

# Register your models here.

pcr_models = [
  Reagent, Flourescence, Control, 
  Assay, AssayList, ExtractionProtocol, 
  Batch, Sample, ThermalCyclerProtocol, 
  Plate, ReagentOrder, ControlOrder, 
  Process, ProcessPlate, Solution,
  Tube, Location,
]

admin.site.register(pcr_models)
