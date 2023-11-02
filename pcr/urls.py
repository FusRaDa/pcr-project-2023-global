from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("create/", views.createBatches, name="create_batches"),
  path("batch-samples/<str:pk>", views.batchSamples, name="batch_samples")
]
