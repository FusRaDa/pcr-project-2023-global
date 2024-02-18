from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

import stripe
from djstripe import webhooks as djstripe_hooks
from djstripe.settings import djstripe_settings
from djstripe.models import Subscription, Customer

from pcr.models.assay import Assay, AssayCode, Control
from pcr.models.batch import Batch
from pcr.models.pcr import Process
from .forms import DeletionForm

from pcr.custom.constants import LIMITS


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
  messages.success(request, f"You've successfully signed up as a premium user.")
  return redirect('batches')

  
@login_required(login_url='login')
def create_portal_session(request):
  try:
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    portal_session = stripe.billing_portal.Session.create(
      customer=request.user.customer.id,
      return_url=f"{get_current_site(request).domain}/subscription-details/",
      # return_url="https://127.0.0.1:8000/subscription-details/",
    )
    return HttpResponseRedirect(portal_session.url)
  except AttributeError:
    return redirect('profile')


# Stripe webhook
# set the only two events in stripe dashboard when live
@csrf_exempt
@djstripe_hooks.handler("checkout.session.completed", "customer.subscription.deleted")
def handle_stripe_sub(request):
  event_dict = json.loads(request.body)

  # print(event_dict['type'])

  if event_dict['type'] == 'checkout.session.completed':
    data = event_dict['data']['object']

    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    # print(djstripe_settings.STRIPE_SECRET_KEY)
    
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


@login_required(login_url='login')
def profile(request):
  assay_count = Assay.objects.filter(user=request.user).count()
  control_count = Control.objects.filter(user=request.user).count()
  assay_code_count = AssayCode.objects.filter(user=request.user).count()
  batch_count = Batch.objects.filter(user=request.user).count()
  process_count = Process.objects.filter(user=request.user).count()

  limit_assay = LIMITS.ASSAY_LIMIT
  limit_control = LIMITS.CONTROL_LIMIT
  limit_assay_code = LIMITS.ASSAY_CODE_LIMIT
  limit_batch = LIMITS.BATCH_LIMIT
  limit_process = LIMITS.PROCESS_LIMIT

  max_assay = LIMITS.MAX_ASSAY_LIMIT
  max_control = LIMITS.MAX_CONTROL_LIMIT
  max_assay_code = LIMITS.MAX_ASSAY_CODE_LIMIT
  max_batch = LIMITS.MAX_BATCH_LIMIT
  max_process = LIMITS.MAX_PROCESS_LIMIT

  limits = []
  limits.append({'name': 'Assays', 'count': assay_count, 'limit': limit_assay, 'premium': max_assay})
  limits.append({'name': 'Controls', 'count': control_count, 'limit': limit_control, 'premium': max_control})
  limits.append({'name': 'Panels', 'count': assay_code_count, 'limit': limit_assay_code, 'premium': max_assay_code})
  limits.append({'name': 'Batches', 'count': batch_count, 'limit': limit_batch, 'premium': max_batch})
  limits.append({'name': 'Processes', 'count': process_count, 'limit': limit_process, 'premium': max_process})

  clear_batch_form = DeletionForm(value=request.user.email)
  clear_process_form = DeletionForm(value=request.user.email)

  if 'clear_batches' in request.POST:
    clear_batch_form = DeletionForm(request.POST, value=request.user.email)
    if clear_batch_form.is_valid():
      batches = Batch.objects.filter(user=request.user, is_extracted=True)
      for batch in batches:
        batch.delete()
    else:
      print(clear_batch_form.errors)

  if 'clear_processes' in request.POST:
    clear_process_form = DeletionForm(request.POST, value=request.user.email)
    if clear_process_form.is_valid():
      processes = Process.objects.filter(user=request.user, is_processed=True)
      for process in processes:
        process.delete()
    else:
      print(clear_process_form.errors)

  context = {'limits': limits, 'clear_batch_form': clear_batch_form, 'clear_process_form': clear_process_form}
  return render(request, 'profile.html', context)

