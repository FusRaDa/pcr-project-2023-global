from django.urls import path
from . import views

urlpatterns = [
    path("subscription-confirm/", views.subscription_confirm, name="subscription_confirm"),
    path("stripe-webhooks/", views.handle_stripe_sub, name="stripe-webhooks"),

    path("profile/", views.profile, name="profile"),
]

