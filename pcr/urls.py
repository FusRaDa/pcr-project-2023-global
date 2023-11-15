from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create-batch/", views.createBatches, name="create_batch"),
  path("delete-batch/<str:username>/<int:pk>/", views.deleteBatch, name="delete_batch"),
  path("batch-samples/<str:username>/<int:pk>/", views.batchSamples, name="batch_samples"),
  path("sample-assay/<str:username>/<int:pk>/", views.editSampleAssay, name="sample_assay"),

  path("extraction-protocols/", views.extraction_protocols, name="extraction_protocols"),
  path("extraction-protocol/<str:username>/<int:pk>/", views.edit_extraction_protocol, name="edit_extraction_protocol"),

  path("assay-codes/", views.assay_codes, name="assay_codes"),
  path("assay-code/<str:username>/<int:pk>/", views.edit_assay_code, name="edit_assay_code"),
]
