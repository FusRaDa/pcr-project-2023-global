from django.urls import path
from .views import items_views, affiliates_views, orders_views

urlpatterns = [
  path('contacts/', affiliates_views.contacts, name='contacts'),
  path('affiliate-program/', affiliates_views.create_contact, name='create_contact'),
  path('edit-contact/<int:pk>/', affiliates_views.edit_contact, name='edit_contact'),

  path('brands/', affiliates_views.brands, name='brands'),
  path('create-brand/', affiliates_views.create_brand, name='create_brand'),
  path('edit-brand/<int:pk>/', affiliates_views.edit_brand, name='edit_brand'),

  path('tags/', items_views.tags, name='tags'),
  path('create-tag/', items_views.create_tag, name='create_tag'),
  path('edit-tag/<int:pk>/', items_views.edit_tag, name='edit_tag'),

  path('kits/', items_views.kits, name='kits'),
  path('create-kit/', items_views.create_kit, name='create_kit'),
  path('edit-kit/<int:pk>/', items_views.edit_kit, name='edit_kit'),
  path('edit-kit-items/<int:pk>/', items_views.edit_kit_items, name='edit_kit_items'),

  path('reviews/<int:pk>', items_views.reviews, name='reviews'),
  path('edit_review/<int:pk>/', items_views.edit_review, name='edit_review'),

  path('create-tube-store/', items_views.create_tube, name='create_tube_store'),
  path('edit-tube-store/<int:pk>/', items_views.edit_tube, name='edit_tube_store'),

  path('create-control-store/', items_views.create_control, name='create_control_store'),
  path('edit-control-store/<int:pk>/', items_views.edit_control, name='edit_control_store'),

  path('create-ladder-store/', items_views.create_ladder, name='create_ladder_store'),
  path('edit-ladder-store/<int:pk>/', items_views.edit_ladder, name='edit_ladder_store'),

  path('create-dye-store/', items_views.create_dye, name='create_dye_store'),
  path('edit-dye-store/<int:pk>/', items_views.edit_dye, name='edit_dye_store'),

  path('create-gel-store/', items_views.create_gel, name='create_gel_store'),
  path('edit-gel-store/<int:pk>/', items_views.edit_gel, name='edit_gel_store'),

  path('create-plate-store/', items_views.create_plate, name='create_plate_store'),
  path('edit-plate-store/<int:pk>/', items_views.edit_plate, name='edit_plate_store'),

  path('create-reagent-store/', items_views.create_reagent, name='create_reagent_store'),
  path('edit-reagent-store/<int:pk>/', items_views.edit_reagent, name='edit_reagent_store'),

  path('', orders_views.store, name='store'),
  path('add-kit-to-order/<int:order_pk>/<int:kit_pk>/', orders_views.add_kit_to_order, name='add_kit_to_order'),
  path('remove-kit-from-order/<int:order_pk>/<int:kit_pk>/', orders_views.remove_kit_from_order, name='remove_kit_from_order'),

  path('orders/', orders_views.orders, name='orders'),
  path('review-order/<int:pk>/', orders_views.review_order, name='review_order'),
  path('view-order/<int:pk>/', orders_views.view_order, name='view_order'),
  path('copy-order/<int:pk>/', orders_views.copy_order, name='copy_order'),

  path('add-to-inventory/<int:order_pk>/<int:kit_pk>/', orders_views.add_to_inventory, name='add_to_inventory'),
]