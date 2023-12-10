from django.urls import path
from . import views

urlpatterns = [
    path("pricing-page/", views.pricing_page, name="pricing_page"),
    path("subscription-confirm/", views.subscription_confirm, name="subscription_confirm"),
    path("subscription-details/", views.create_portal_session, name="subscription_details"),

    path("stripe-webhooks/", views.handle_stripe_sub, name="stripe-webhooks"),
]

