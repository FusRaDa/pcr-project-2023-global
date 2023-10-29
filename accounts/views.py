from django.shortcuts import render, redirect
from .forms import CreateUserForm, ProfileForm, AssignRolesForm
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .decorators import unauthenticated_user, manager_only, lab_access
from django.contrib.auth.models import Group, User

from .tokens import account_activation_token
from .models import EmailOrUsernameModelBackend, Profile


# login user with their username or email and password
@unauthenticated_user
def loginPage(request):

  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = EmailOrUsernameModelBackend.authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('master_sheet')
    else:
      messages.info(request, 'username OR password is incorrect')

  context = {}
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
    messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
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

    Profile.objects.create(
      username=user,
      email=user.email,
      first_name=user.first_name,
      last_name=user.last_name,
    )

    default_group = Group.objects.get(name="Incoming")
    user.groups.add(default_group)

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
      return redirect('login')
    
    else:
      for error in list(form.errors.values()):
        messages.error(request, error)

  context = {'form': form}
  return render(request, "register.html", context)
  

# logout user
def logoutUser(request):
  logout(request)
  return redirect('login')


# view dashboard of all users and work progress
@login_required(login_url='login')
@lab_access
def accounts(request):

  is_manager = request.user.groups.filter(name="Manager").exists()

  incomings = User.objects.filter(groups__name="Incoming")

  managers = User.objects.filter(groups__name="Manager")

  technicians = User.objects.filter(groups__name="Technician")

  context = {'incomings': incomings, 'managers': managers, 'technicians': technicians, 'is_manager': is_manager}
  return render(request, "accounts.html", context)


# view user profile page
@login_required(login_url='login')
def profile(request):
   user = request.user.profile
   form = ProfileForm(instance=user)

   is_incoming = request.user.groups.filter(name="Incoming").exists()

   if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()

      user_model = User.objects.filter(username=request.user)

      user_model.update(
        first_name=user.first_name,
        last_name=user.last_name
      )

      return redirect('accounts')

   context = {'form': form, 'is_incoming': is_incoming}
   return render(request, "profile.html", context)


@login_required(login_url='login')
@manager_only
def assignUserRoles(request, pk):

  user = User.objects.get(pk=pk)
  form = AssignRolesForm(instance=user)

  if request.method == "POST":
    form = AssignRolesForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('accounts')

  context = {'form': form}
  return render(request, "roles.html", context)


@login_required(login_url='login')
@lab_access
def view(request, username):

  user = User.objects.get(username=username)

  context = {'user': user}
  return render(request, "user.html", context)