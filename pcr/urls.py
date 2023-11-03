from django.urls import path
from . import views

urlpatterns = [
  path("", views.viewBatches, name="batches"),
  path("batch/", views.createBatches, name="batch"),
  path("batch/<str:pk>", views.batchSamples, name="batch_samples")
]
