from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

import stripe
from djstripe import webhooks as djstripe_hooks
from djstripe.settings import djstripe_settings
from djstripe.models import Product, Subscription, Customer, APIKey

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


# Stripe webhook
# set the only two events in stripe dashboard when live
@csrf_exempt
@djstripe_hooks.handler("checkout.session.completed", "customer.subscription.deleted")
def handle_stripe_sub(request):

  event_dict = json.loads(request.body)

  print(event_dict['type'])

  if event_dict['type'] == 'checkout.session.completed':
    data = event_dict['data']['object']

    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    print(djstripe_settings.STRIPE_SECRET_KEY)
    
    try:
      subscription_holder = get_user_model().objects.get(id=data['client_reference_id'])

      if subscription_holder.subscription == None and subscription_holder.customer == None:
        subscription = stripe.Subscription.retrieve(data['subscription'])
        djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

        subscription_holder.subscription = djstripe_subscription
        subscription_holder.customer = djstripe_subscription.customer
        subscription_holder.save()
    except ObjectDoesNotExist:
      pass

  if event_dict['type'] == 'customer.subscription.deleted':
    data = event_dict['data']['object']

    try:
      subscription = Subscription.objects.get(id=data['id'])
      customer = Customer.objects.get(id=data['customer'])

      subscription.delete()
      customer.delete()
    except ObjectDoesNotExist:
      pass

  return HttpResponse(status=200)
