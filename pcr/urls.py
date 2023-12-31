from django.urls import path
from .views import batch_views, assay_code_views, extraction_protocol_views, assay_views, inventory_views, pcr_views


urlpatterns = [
  path("", batch_views.viewBatches, name="batches"),
  path("create-batch/", batch_views.createBatches, name="create_batch"),
  path("batch-samples/<str:username>/<int:pk>/", batch_views.batchSamples, name='batch_samples'),
  path("sample-assay/<str:username>/<int:pk>/", batch_views.editSampleAssay, name='sample_assay'),
  path("batch-paperwork/<str:username>/<int:pk>/", batch_views.batch_paperwork, name='batch_paperwork'),

  path("extraction-protocols/", extraction_protocol_views.extraction_protocols, name='extraction_protocols'),
  path("create-extraction-protocol/", extraction_protocol_views.create_extraction_protocol, name='create_extraction_protocol'),
  path("edit-extraction-protocol/<str:username>/<int:pk>/", extraction_protocol_views.edit_extraction_protocol, name='edit_extraction_protocol'),
  path("amount-extraction-protocol/<str:username>/<int:pk>/", extraction_protocol_views.extraction_protocol_through, name='extraction_protocol_through'),

  path("assay-codes/", assay_code_views.assay_codes, name='assay_codes'),
  path("create-assay-code/", assay_code_views.create_assay_code, name='create_assay_code'),
  path("assay-code/<str:username>/<int:pk>/", assay_code_views.edit_assay_code, name='edit_assay_code'),

  path("assays/", assay_views.assays, name='assays'),
  path("create-assay/", assay_views.create_assay, name='create_assay'),
  path("edit-assay/<str:username>/<int:pk>/", assay_views.edit_assay, name='edit_assay'),
  path("amount-assay/<str:username>/<int:pk>/", assay_views.assay_through, name='assay_through'),

  path("fluorescence/", assay_views.fluorescence, name='fluorescence'),
  path("create-fluorescence/", assay_views.create_fluorescence, name='create_fluorescence'),
  path("edit-fluorescence/<str:username>/<int:pk>/", assay_views.edit_fluorescence, name='edit_fluorescence'),

  path("controls/", assay_views.controls, name='controls'),
  path("create-control/", assay_views.create_control, name='create_control'),
  path("edit-control/<str:username>/<int:pk>/", assay_views.edit_control, name='edit_control'),

  path("locations/", inventory_views.locations, name='locations'),
  path("create-location/", inventory_views.create_location, name='create_location'),
  path("edit-location/<str:username>/<int:pk>/", inventory_views.edit_location, name='edit_location'),

  path("plates/", inventory_views.plates, name='plates'),
  path("create-plate/", inventory_views.create_plate, name='create_plate'),
  path("edit-plate/<str:username>/<int:pk>/", inventory_views.edit_plate, name='edit_plate'),

  path("tubes/", inventory_views.tubes, name='tubes'),
  path("create-tube/", inventory_views.create_tube, name='create_tube'),
  path("edit-tube/<str:username>/<int:pk>/", inventory_views.edit_tube, name='edit_tube'),

  path("reagents/", inventory_views.reagents, name='reagents'),
  path("create-reagent/", inventory_views.create_reagent, name='create_reagent'),
  path("edit-reagent/<str:username>/<int:pk>/", inventory_views.edit_reagent, name='edit_reagent'),

  path("tcprotocols/", pcr_views.tcprotocols, name='tcprotocols'),
  path("create-tcprotocol/", pcr_views.create_tcprotocol, name='create_tcprotocol'),
  path("edit_tcprotocol/<str:username>/<int:pk>/", pcr_views.edit_tcprotocol, name='edit_tcprotocol'),

  path("extracted-batches/", pcr_views.extracted_batches, name='extracted_batches'),
  path("add-batch-samples/<str:username>/<int:process_pk>/<int:batch_pk>/", pcr_views.add_batch_samples, name='add_batch_samples'),
  path("add-sample-to-process/<str:username>/<int:process_pk>/<int:sample_pk>/", pcr_views.add_sample_to_process, name='add_sample_to_process'),
  path("remove-sample-from-process/<str:username>/<int:process_pk>/<int:sample_pk>/", pcr_views.remove_sample_from_process, name='remove_sample_from_process'),
  path("review-process/<str:username>/<int:pk>/", pcr_views.review_process, name='review_process'),
]
