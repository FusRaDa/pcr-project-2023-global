from django.contrib import admin

from .models.inventory import Plate, Tube, Reagent, Location
from .models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction
from .models.assay import Assay, AssayCode, ReagentAssay, Fluorescence, Control
from .models.batch import Batch, Sample
from .models.pcr import ThermalCyclerProtocol, Process

# Register your models here.

models = [
  Reagent, Fluorescence, Control, 
  Assay, AssayCode, ExtractionProtocol, 
  Batch, Sample, ThermalCyclerProtocol, 
  Plate, ReagentAssay, Process, Tube, 
  Location, ReagentExtraction, TubeExtraction,
]

admin.site.register(models)
