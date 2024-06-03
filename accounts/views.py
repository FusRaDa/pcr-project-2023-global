from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

from google.auth.transport import requests
from google.oauth2 import id_token

from .decorators import unauthenticated_user
from users.models import User

from .tokens import account_activation_token
from .models import EmailOrUsernameModelBackend
from .forms import CreateUserForm, LoginUserForm
from analytics.functions import record_user_login
from .functions import is_verified
from pcr.custom.constants import LIMITS


# login user with their username or email and password
@unauthenticated_user
def loginPage(request):

  form = LoginUserForm()
  if request.method == "POST":
    form = LoginUserForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      user = EmailOrUsernameModelBackend.authenticate(request, username=username, password=password)

      if user is not None and not user.is_active:
        messages.info(request, 'Please verify your email.')

      if user is not None:
        record_user_login(user)
        login(request, user)
        return redirect('inventory_report')
      else:
        messages.info(request, '**username and/or password is incorrect.**')

    else:
      print(form.errors)

  context = {'form': form}
  return render(request, "login.html", context)
  

# this function is to send the activation email - https://github.com/leemunroe/responsive-html-email-template
def activateEmail(request, user, to_email):
  mail_subject = 'Welcome to PCRprep!'
  message = render_to_string('template_activate_account.html', {
    'user': user.username,
    'domain': get_current_site(request).domain,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': account_activation_token.make_token(user),
    'protocol': 'https' if request.is_secure() else 'http'
  })
  email = EmailMessage(mail_subject, message, to=[to_email], from_email=settings.EMAIL_ALIAS)
  if email.send():
    messages.success(request, f'Welcome {user}! Check your email: {to_email} and click on the\
      received activation link to confirm and complete the registration. Note: Check your spam folder.')
  else:
    messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


# once the activation email's url has been clicked, activate their account
def activate(request, uidb64, token):
  User = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()

    # create_test_objects(user) # REMOVE THIS FROM PRODUCTION - FOR TESTING PURPOSES ONLY

    messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.')
    return redirect('login')
  else:
    messages.error(request, 'Activation link is invalid!')
  
  return redirect('login')


# register new user
@unauthenticated_user
def register(request):
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
  limits.append({'name': 'Assays', 'limit': limit_assay, 'premium': max_assay})
  limits.append({'name': 'Controls', 'limit': limit_control, 'premium': max_control})
  limits.append({'name': 'Panels', 'limit': limit_assay_code, 'premium': max_assay_code})
  limits.append({'name': 'Batches', 'limit': limit_batch, 'premium': max_batch})
  limits.append({'name': 'Processes', 'limit': limit_process, 'premium': max_process})
  
  form = CreateUserForm()

  if request.method == "POST":

    form = CreateUserForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')

      if User.objects.filter(email=email).exists():
        messages.error(request, 'This email already exists, would you like to reset your password?')
        return redirect('login')
      
      try:
        validate_email(email)
      except ValidationError:
        messages.error(request, 'This is an invalid email. Please try again.')
        return redirect('register')
      
      if not is_verified(email):
        messages.error(request, 'This is an invalid email. Please try again.')
        return redirect('register')

      user = form.save(commit=False)
      user.is_active=False
      user.save()
      activateEmail(request, user, email)
      return redirect('login')
    else:
      print(form.errors)

  if settings.DEBUG:
    uri = "http://localhost:8000"
  else:
    domain = get_current_site(request).domain
    uri = 'https://' + domain

  context = {'form': form, 'limits': limits, 'uri': uri}
  return render(request, "register.html", context)


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('login')
  

# logout user
def logoutUser(request):
  logout(request)
  return redirect('login')


def custom_404(request):
  return render(request, '404.html', status=404)


def custom_500(request):
  return render(request, '500.html', status=500)