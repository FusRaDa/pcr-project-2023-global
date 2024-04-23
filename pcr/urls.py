from django.urls import path
from .views import batch_views, assay_code_views, extraction_protocol_views, assay_views, inventory_views, pcr_views, dashboard_views


urlpatterns = [
  path("batches/", batch_views.batches, name="batches"),
  path("create-batch/", batch_views.create_batch, name="create_batch"),
  path("batch-samples/<int:pk>/", batch_views.batch_samples, name='batch_samples'),
  path("sample-assay/<int:pk>/", batch_views.sample_assay, name='sample_assay'),
  path("batch-paperwork/<int:pk>/", batch_views.batch_paperwork, name='batch_paperwork'),

  path("extraction-protocols/", extraction_protocol_views.extraction_protocols, name='extraction_protocols'),
  path("create-extraction-protocol/", extraction_protocol_views.create_extraction_protocol, name='create_extraction_protocol'),
  path("edit-extraction-protocol/<int:pk>/", extraction_protocol_views.edit_extraction_protocol, name='edit_extraction_protocol'),
  path("add-tube-extraction/<int:protocol_pk>/<int:tube_pk>/", extraction_protocol_views.add_tube_extraction, name='add_tube_extraction'),
  path("remove-tube-extraction/<int:protocol_pk>/<int:tube_pk>/", extraction_protocol_views.remove_tube_extraction, name='remove_tube_extraction'),
  path("add-reagent-extraction/<int:protocol_pk>/<int:reagent_pk>/", extraction_protocol_views.add_reagent_extraction, name='add_reagent_extraction'),
  path("remove-reagent-extraction/<int:protocol_pk>/<int:reagent_pk>/", extraction_protocol_views.remove_reagent_extraction, name='remove_reagent_extraction'),
  path("tubes-in-extraction/<int:pk>/", extraction_protocol_views.tubes_in_extraction, name='tubes_in_extraction'),
  path("reagents-in-extraction/<int:pk>/", extraction_protocol_views.reagents_in_extraction, name='reagents_in_extraction'),

  path("assay-codes/", assay_code_views.assay_codes, name='assay_codes'),
  path("create-assay-code/", assay_code_views.create_assay_code, name='create_assay_code'),
  path("edit-assay-code/<int:pk>/", assay_code_views.edit_assay_code, name='edit_assay_code'),

  path("assays/", assay_views.assays, name='assays'),
  path("create-assay/", assay_views.create_assay, name='create_assay'),
  path("edit-assay/<int:pk>/", assay_views.edit_assay, name='edit_assay'),
  path("add-control-assay/<int:assay_pk>/<int:control_pk>/", assay_views.add_control_assay, name='add_control_assay'),
  path("remove-control-assay/<int:assay_pk>/<int:control_pk>/", assay_views.remove_control_assay, name='remove_control_assay'),
  path("add-reagent-assay/<int:assay_pk>/<int:reagent_pk>/", assay_views.add_reagent_assay, name='add_reagent_assay'),
  path("remove-reagent-assay/<int:assay_pk>/<int:reagent_pk>/", assay_views.remove_reagent_assay, name='remove_reagent_assay'),
  
  path("reagents-in-assay/<int:pk>/", assay_views.reagents_in_assay, name='reagents_in_assay'),
  path("controls-in-assay/<int:pk>/", assay_views.controls_in_assay, name='controls_in_assay'),

  path("fluorescence/", assay_views.fluorescence, name='fluorescence'),
  path("create-fluorescence/", assay_views.create_fluorescence, name='create_fluorescence'),
  path("edit-fluorescence/<int:pk>/", assay_views.edit_fluorescence, name='edit_fluorescence'),

  path("controls/", assay_views.controls, name='controls'),
  path("create-control/", assay_views.create_control, name='create_control'),
  path("edit-control/<int:pk>/", assay_views.edit_control, name='edit_control'),

  path("locations/", inventory_views.locations, name='locations'),
  path("create-location/", inventory_views.create_location, name='create_location'),
  path("edit-location/<int:pk>/", inventory_views.edit_location, name='edit_location'),

  path("ladders/", inventory_views.ladders, name='ladders'),
  path("create-ladder/", inventory_views.create_ladder, name='create_ladder'),
  path("edit-ladder/<int:pk>/", inventory_views.edit_ladder, name='edit_ladder'),

  path("dyes/", inventory_views.dyes, name='dyes'),
  path("create-dye/", inventory_views.create_dye, name='create_dye'),
  path("edit-dye/<int:pk>/", inventory_views.edit_dye, name='edit_dye'),

  path("gels/", inventory_views.gels, name='gels'),
  path("create-gel/", inventory_views.create_gel, name='create_gel'),
  path("edit-gel/<int:pk>/", inventory_views.edit_gel, name='edit_gel'),

  path("plates/", inventory_views.plates, name='plates'),
  path("create-plate/", inventory_views.create_plate, name='create_plate'),
  path("edit-plate/<int:pk>/", inventory_views.edit_plate, name='edit_plate'),

  path("tubes/", inventory_views.tubes, name='tubes'),
  path("create-tube/", inventory_views.create_tube, name='create_tube'),
  path("edit-tube/<int:pk>/", inventory_views.edit_tube, name='edit_tube'),

  path("reagents/", inventory_views.reagents, name='reagents'),
  path("create-reagent/", inventory_views.create_reagent, name='create_reagent'),
  path("edit-reagent/<int:pk>/", inventory_views.edit_reagent, name='edit_reagent'),

  path("tcprotocols/", pcr_views.tcprotocols, name='tcprotocols'),
  path("create-tcprotocol/", pcr_views.create_tcprotocol, name='create_tcprotocol'),
  path("edit-tcprotocol/<int:pk>/", pcr_views.edit_tcprotocol, name='edit_tcprotocol'),

  path("extracted-batches/", pcr_views.extracted_batches, name='extracted_batches'),
  path("add-batch-samples/<int:process_pk>/<int:batch_pk>/", pcr_views.add_batch_samples, name='add_batch_samples'),
  path("add-sample-to-process/<int:process_pk>/<int:sample_pk>/", pcr_views.add_sample_to_process, name='add_sample_to_process'),
  path("remove-sample-from-process/<int:process_pk>/<int:sample_pk>/", pcr_views.remove_sample_from_process, name='remove_sample_from_process'),
  path("review-process/<int:pk>/", pcr_views.review_process, name='review_process'),
  path("process-paperwork/<int:pk>/", pcr_views.process_paperwork, name='process_paperwork'),

  path('processes/', pcr_views.processes, name='processes'),
  path('pcr-paperwork/<int:pk>/', pcr_views.pcr_paperwork, name='pcr_paperwork'),

  path('controls-display/', dashboard_views.controls_display, name='controls_display'),
  path('batches-display/', dashboard_views.batches_display, name='batches_display'),
  path('processes-display/', dashboard_views.processes_display, name='processes_display'),

  path('ladders-display/', dashboard_views.ladders_display, name='ladders_display'),
  path('dyes-display/', dashboard_views.dyes_display, name='dyes_display'),
  path('plates-display/', dashboard_views.plates_display, name='plates_display'),
  path('gels-display/', dashboard_views.gels_display, name='gels_display'),
  path('tubes-display/', dashboard_views.tubes_display, name='tubes_display'),
  path('reagents-display/', dashboard_views.reagents_display, name='reagents_display'),

  path('assays-chart/', dashboard_views.assays_chart, name='assays_chart'),
  path('panels-chart/', dashboard_views.panels_chart, name='panels_chart'),

  path('dashboard/', dashboard_views.inventory_report, name='inventory_report'),
]
