from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create-batch/", views.createBatches, name="create_batch"),
  path("delete-batch/<str:username>/<int:pk>/", views.deleteBatch, name="delete_batch"),
  path("batch-samples/<str:username>/<int:pk>/", views.batchSamples, name="batch_samples"),
  path("sample-assay/<str:username>/<int:pk>/", views.editSampleAssay, name="sample_assay"),

  path("extraction-protocols/", views.extraction_protocols, name="extraction_protocols"),
  path("extraction-protocol-create/", views.create_extraction_protocol, name="create_extraction_protocol"),
  path("extraction-protocol/<str:username>/<int:pk>/", views.edit_extraction_protocol, name="edit_extraction_protocol"),
  path("extraction-protocol-through/<str:username>/<int:pk>/", views.extraction_protocol_through, name="extraction_protocol_through"),
  path("extraction-protocol-delete/<str:username>/<int:pk>/", views.delete_extraction_protocol, name="delete_extraction_protocol"),

  path("assay-codes/", views.assay_codes, name="assay_codes"),
  path("assay-code-create/", views.create_assay_code, name="create_assay_code"),
  path("assay-code/<str:username>/<int:pk>/", views.edit_assay_code, name="edit_assay_code"),
  path("assay-code-delete/<str:username>/<int:pk>/", views.delete_assay_code, name="delete_assay_code"),
]
