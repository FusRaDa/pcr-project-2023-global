from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .decorators import unauthenticated_user
from users.models import User

from .tokens import account_activation_token
from .models import EmailOrUsernameModelBackend
from .forms import CreateUserForm, LoginUserForm
from .functions import create_test_objects
from analytics.functions import record_user_login


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
        return redirect('reagents')
      else:
        messages.info(request, '**username and/or password is incorrect.**')

    else:
      print(form.errors)

  context = {'form': form}
  return render(request, "login.html", context)
  

# this function is to send the activation email
def activateEmail(request, user, to_email):
  mail_subject = 'Activate your user account.'
  message = render_to_string('template_activate_account.html', {
    'user': user.username,
    'domain': get_current_site(request).domain,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': account_activation_token.make_token(user),
    'protocol': 'https' if request.is_secure() else 'http'
  })
  email = EmailMessage(mail_subject, message, to=[to_email])
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

    create_test_objects(user) # REMOVE THIS FROM PRODUCTION - FOR TESTING PURPOSES ONLY

    messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
    return redirect('login')
  else:
    messages.error(request, 'Activation link is invalid!')
  
  return redirect('login')


# register new user
@unauthenticated_user
def register(request):
  
  form = CreateUserForm()

  if request.method == "POST":

    form = CreateUserForm(request.POST)
    if form.is_valid():

      email = form.cleaned_data.get('email')
      if User.objects.filter(email=email).exists():
        messages.error(request, 'This email already exists, would you like to reset your password?')
        return redirect('login')

      user = form.save(commit=False)
      user.is_active=False
      user.save()
      activateEmail(request, user, form.cleaned_data.get('email'))
      return redirect('reagents')
    
    else:
      for error in list(form.errors.values()):
        messages.error(request, error)

  context = {'form': form}
  return render(request, "register.html", context)
  

# logout user
def logoutUser(request):
  logout(request)
  return redirect('login')