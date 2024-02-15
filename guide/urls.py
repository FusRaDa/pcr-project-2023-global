from django.urls import path
from . import views

urlpatterns = [
  path("", views.landing_page, name='landing_page'),
  path("about/", views.about_page, name='about_page'),
  path("faq/", views.faq_page, name='faq_page'),
  path("guide/", views.guide_page, name='guide_page'),
  path("privacy-policy/", views.privacy_policy, name='privacy_policy'),
  path("subscription-policy/", views.subscription_policy, name='subscription_policy'),
  path("terms-conditions/", views.terms_conditions, name='terms_conditions')
]