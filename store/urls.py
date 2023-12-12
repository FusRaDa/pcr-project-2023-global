from django.urls import path
from .views import items_views, affiliates_views, orders_views

urlpatterns = [
  path('contacts/', ),
  path('create-kit/', items_views.create_kit, name='create_kit'),
]