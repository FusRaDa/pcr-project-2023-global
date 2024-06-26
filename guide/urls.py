from django.urls import path
from . import views

urlpatterns = [
  path("about/", views.about_page, name='about_page'),
  path("faq/", views.faq_page, name='faq_page'),
  path("privacy-policy/", views.privacy_policy, name='privacy_policy'),
  path("subscription-policy/", views.subscription_policy, name='subscription_policy'),
  path("terms-conditions/", views.terms_conditions, name='terms_conditions'),
  path("email-opt-in/", views.email_opt_in, name='email_opt_in'),

  path("guide/", views.guide_page, name='guide_page'),
  path("guide/inventory-guide/", views.inventory_guide, name='inventory_guide'),
  path("guide/tests-guide/", views.tests_guide, name='tests_guide'),
  path("guide/protocols-guide/", views.protocols_guide, name='protocols_guide'),
  path("guide/extraction-guide/", views.extraction_guide, name='extraction_guide'),
  path("guide/pcr-guide/", views.pcr_guide, name='pcr_guide'),

  path("articles/", views.articles_page, name='articles_page'),
  path("articles/pcrmastermix/", views.pcrmastermix_article, name='pcrmastermix_article'),
]