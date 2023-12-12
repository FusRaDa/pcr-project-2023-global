from django.urls import path
from .views import items_views, affiliates_views, orders_views

urlpatterns = [
  path('contacts/', affiliates_views.contacts, name='contacts'),
  path('create-contact/', affiliates_views.create_contact, name='create_contact'),
  path('edit-contact/<int:pk>/', affiliates_views.edit_contact, name='edit_contact'),

  path('brands/', affiliates_views.brands, name='brands'),
  path('create-brand/', affiliates_views.create_brand, name='create_brand'),
  path('edit-brand/<int:pk>/', affiliates_views.edit_brand, name='edit_brand'),

  path('kits/', items_views.kits, name='kits'),
  path('create-kit/', items_views.create_kit, name='create_kit'),
  path('edit-kit/<int:pk>/', items_views.edit_kit, name='edit_kit'),

  path('create-tube-store/', items_views.create_tube, name='create_tube_store'),
  path('edit-tube-store/<int:pk>/', items_views.edit_tube, name='edit_tube_store'),

  path('create-plate-store/', items_views.create_plate, name='create_plate_store'),
  path('edit-plate-store/<int:pk>/', items_views.edit_plate, name='edit_plate_store'),

  path('create-reagent-store/', items_views.create_reagent, name='create_reagent_store'),
  path('edit-reagent-store/<int:pk>/', items_views.edit_reagent, name='edit_reagent_store'),

  path('orders/', orders_views.orders, name='orders'),
  path('edit-order/<str:username>/<int:pk>/', orders_views.edit_order, name='edit_order'),
]