from django.urls import path
from . import views

urlpatterns = [
  path("", views.landing_page, name='landing_page'),
  path("about/", views.about_page, name='about_page'),
  path("faq/", views.faq_page, name='faq_page'),
  path("guide/", views.guide_page, name='guide_page'),
]