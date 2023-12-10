from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

import stripe
from djstripe import webhooks as djstripe_hooks
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
  if session_id == None:
     return redirect('batches')
 
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
  return redirect('batches')

  
@login_required
def create_portal_session(request):
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    portal_session = stripe.billing_portal.Session.create(
      customer=request.user.customer.id,
      return_url="https://127.0.0.1:8000/subscription-details/",
    )
    return HttpResponseRedirect(portal_session.url)


# Stripe webhooks
@csrf_exempt
@djstripe_hooks.handler("customer.subscription.deleted", "checkout.session.completed")
def handle_stripe_events(request):
  print("customer now has a subscription")
  json_data = json.loads(request.body)
  print(json_data)

  return HttpResponse(status=200)
