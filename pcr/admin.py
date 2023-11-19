from django.contrib import admin

from .models.inventory import Plate, Tube, Reagent, Location
from .models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction
from .models.assay import Assay, AssayCode, ReagentAssay, Flourescence, Control
from .models.batch import Batch, Sample
from .models.pcr import ThermalCyclerProtocol, Process, ProcessPlate

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
