from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import stripe
from djstripe.settings import djstripe_settings

from djstripe.models import Subscription
from djstripe.models import Product

@login_required(login_url='login')
def pricing_page(request):
  context = {'products': Product.objects.all()}
  return render(request, 'pricing_page.html', context)


@login_required(login_url='login')
def subscription_confirm(request):
  # set our stripe keys up
  stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

  # get the session id from the URL and retrieve the session object from Stripe
  session_id = request.GET.get("session_id")
  session = stripe.checkout.Session.retrieve(session_id)

  # get the subscribing user from the client_reference_id we passed in above
  client_reference_id = int(session.client_reference_id)
  subscription_holder = get_user_model().objects.get(id=client_reference_id)
  # sanity check that the logged in user is the one being updated
  assert subscription_holder == request.user

  # get the subscription object form Stripe and sync to djstripe
  subscription = stripe.Subscription.retrieve(session.subscription)
  djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

  # set the subscription and customer on our user
  subscription_holder.subscription = djstripe_subscription
  subscription_holder.customer = djstripe_subscription.customer
  subscription_holder.save()

  # show a message to the user and redirect
  messages.success(request, f"You've successfully signed up. Thanks for the support!")
  return HttpResponseRedirect(reverse("subscription_details"))