from django.urls import path
from .views.batch_views import viewBatches, createBatches, deleteBatch, batchSamples, editSampleAssay
from .views.assay_code_views import assay_codes, create_assay_code, edit_assay_code, delete_assay_code
from .views.extraction_protocol_views import extraction_protocols, create_extraction_protocol, edit_extraction_protocol, extraction_protocol_through, delete_extraction_protocol
from .views.assay_views import assays, create_assay, edit_assay, assay_through, delete_assay
from .views.inventory_views import (
  locations, create_location, edit_location, delete_location, 
  plates, create_plate, edit_plate, delete_plate, 
  tubes, create_tube, edit_tube, delete_tube, 
  reagents, create_reagent, edit_reagent, delete_reagent)

urlpatterns = [
  path("", viewBatches, name="batches"),
  path("create-batch/", createBatches, name="create_batch"),
  path("delete-batch/<str:username>/<int:pk>/", deleteBatch, name="delete_batch"),
  path("batch-samples/<str:username>/<int:pk>/", batchSamples, name="batch_samples"),
  path("sample-assay/<str:username>/<int:pk>/", editSampleAssay, name="sample_assay"),

  path("extraction-protocols/", extraction_protocols, name="extraction_protocols"),
  path("create-extraction-protocol/", create_extraction_protocol, name="create_extraction_protocol"),
  path("extraction-protocol/<str:username>/<int:pk>/", edit_extraction_protocol, name="edit_extraction_protocol"),
  path("quantify-extraction-protocol/<str:username>/<int:pk>/", extraction_protocol_through, name="extraction_protocol_through"),
  path("delete-extraction-protocol/<str:username>/<int:pk>/", delete_extraction_protocol, name="delete_extraction_protocol"),
    
  path("assay-codes/", assay_codes, name="assay_codes"),
  path("create-assay-code/", create_assay_code, name="create_assay_code"),
  path("assay-code/<str:username>/<int:pk>/", edit_assay_code, name="edit_assay_code"),
  path("delete-assay-code/<str:username>/<int:pk>/", delete_assay_code, name="delete_assay_code"),

  path("assays/", assays, name="assays"),
  path("create-assay/", create_assay, name="create_assay"),
  path("assay/<str:username>/<int:pk>/", edit_assay, name="edit_assay"),
  path("quantify-assay/<str:username>/<int:pk>/", assay_through, name="assay_through"),
  path("delete-assay/<str:username>/<int:pk>/", delete_assay, name="delete_assay"),

  path("locations/", locations, name="locations"),
  path("create_location/", create_location, name="create_location"),
  path("edit_location/<str:username>/<int:pk>/", edit_location, name="edit_location"),
  path("delete_location/<str:username>/<int:pk>/", delete_location, name="delete_location"),

  path("plates/", plates, name="plates"),
  path("create_plate/", create_plate, name="create_plate"),
  path("edit_plate/<str:username>/<int:pk>/", edit_plate, name="edit_plate"),
  path("delete_plate/<str:username>/<int:pk>/", delete_plate, name="delete_plate"),

  path("tubes/", tubes, name="tubes"),
  path("create_tube/", create_tube, name="create_tube"),
  path("edit_tube/<str:username>/<int:pk>/", edit_tube, name="edit_tube"),
  path("delete_tube/<str:username>/<int:pk>/", delete_tube, name="delete_tube"),

  path("reagents/", reagents, name="reagents"),
  path("create_reagent/", create_reagent, name="create_reagent"),
  path("edit_reagent/<str:username>/<int:pk>/", edit_reagent, name="edit_reagent"),
  path("delete_reagent/<str:username>/<int:pk>/", delete_reagent, name="delete_reagent"),
]
