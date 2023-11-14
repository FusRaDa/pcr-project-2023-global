from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create-batch/", views.createBatches, name="create_batch"),
  path("delete-batch/<str:username>/<int:pk>/", views.deleteBatch, name="delete_batch"),
  path("batch-samples/<str:username>/<int:pk>/", views.batchSamples, name="batch_samples"),
  path("sample-assay/<str:username>/<int:pk>/", views.editSampleAssay, name="sample_assay"),
  path("extraction-protocols/", views.extraction_protocols, name="extraction_protocols"),
  path("assay-codes/", views.assay_codes, name="assay_codes"),
]
