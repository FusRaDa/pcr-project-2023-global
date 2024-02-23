from django.urls import path
from . import views

urlpatterns = [
  path("", views.landing_page, name='landing_page'),
  path("about/", views.about_page, name='about_page'),
  path("faq/", views.faq_page, name='faq_page'),
  path("privacy-policy/", views.privacy_policy, name='privacy_policy'),
  path("subscription-policy/", views.subscription_policy, name='subscription_policy'),
  path("terms-conditions/", views.terms_conditions, name='terms_conditions'),

  path("guide/", views.guide_page, name='guide_page'),
  path("guide/inventory-guide/", views.inventory_guide, name='inventory_guide'),
  path("guide/tests-guide/", views.tests_guide, name='tests_guide'),
  path("guide/protocols-guide.html", views.protocols_guide, name='protocols_guide'),
  path("guide/extraction-guide.html", views.extraction_guide, name='extraction_guide'),
  path("guide/pcr-guide.html", views.pcr_guide, name='pcr_guide'),
]