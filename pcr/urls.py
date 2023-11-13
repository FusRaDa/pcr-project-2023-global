from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create-batch/", views.createBatches, name="create_batch"),
  path("delete-batch/<str:username>/<int:pk>/", views.deleteBatch, name="delete_batch"),
  path("batch-samples/<str:username>/<int:pk>/", views.batchSamples, name="batch_samples"),
  path("sample-assay/<str:username>/<int:pk>/", views.editSampleAssay, name="sample_assay"),
  path("protocols/", views.protocols, name="protocols"),
]
