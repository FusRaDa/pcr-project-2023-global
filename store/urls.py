from django.urls import path
from .views import items_views

url_patterns = [
  path('create-kit', items_views.create_kit, name='create_kit'),
]