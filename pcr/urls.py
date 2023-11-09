from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create-batch/", views.createBatches, name="create_batch"),
  path("batch-samples/<int:pk>/", views.batchSamples, name="batch_samples")
]
