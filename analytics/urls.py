from django.urls import path
from . import views

urlpatterns = [
  path("dashboard/", views.dashboard, name='dashboard'),
  path("users/", views.users, name='users'),
  path("manage-user/<int:pk>/", views.manage_user, name='manage_user')
]