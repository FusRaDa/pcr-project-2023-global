from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
import datetime
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from users.models import User
from .models import LoginList
from .forms import SearchUserForm, ManageUserForm

# Create your views here.
@staff_member_required(login_url='login')
def dashboard(request):
  user_count = User.objects.count()
  active_count = User.objects.filter(is_active=True).count()
  sub_count = User.objects.filter(subscription__isnull=False, customer__isnull=False).count()
  login_list = LoginList.objects.all().order_by('-date')[:30][::-1] # latest thirty rows

  dates = []
  logins = []
  for val in login_list:
    dates.append(val.date_str)
    logins.append(val.logins)

  json_dates = json.dumps(dates)

  context = {'user_count': user_count, 'active_count': active_count, 'sub_count': sub_count, 'login_list': login_list, 'json_dates': json_dates, 'logins': logins}
  return render(request, 'dashboard.html', context)


@staff_member_required(login_url='login')
def users(request):
  users = User.objects.all().order_by('-date_joined')

  form = SearchUserForm()
  if request.method == 'GET':
    form = SearchUserForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      is_staff = form.cleaned_data['is_staff']
      is_active = form.cleaned_data['is_active']
      is_superuser = form.cleaned_data['is_superuser']
      can_review = form.cleaned_data['can_review']
      is_subscribed = form.cleaned_data['is_subscribed']

      last_login_start = form.cleaned_data['last_login_start']
      last_login_end = form.cleaned_data['last_login_end']

      filters = {}
      if is_staff:
        filters['is_staff'] = is_staff
      if is_active:
        filters['is_active'] = is_active
      if is_superuser:
        filters['is_superuser'] = is_superuser
      if can_review:
        filters['can_review'] = can_review
  
      if last_login_start and not last_login_end:
        day = last_login_start + datetime.timedelta(days=1)
        filters['last_login__range'] = [last_login_start, day]
      
      if last_login_end and not last_login_start:
        day = last_login_end + datetime.timedelta(days=1)
        filters['last_login__range'] = [last_login_end, day]

      if last_login_start and last_login_end:
        last_login_end += datetime.timedelta(days=1)
        filters['last_login__range'] = [last_login_start, last_login_end]

      if is_subscribed == 'False':
        users = User.objects.filter(**filters).filter(subscription__isnull=True, customer__isnull=True).filter((Q(username__icontains=text_search) | Q(first_name__icontains=text_search) | Q(last_name__icontains=text_search) | Q(email__icontains=text_search))).order_by('-date_joined')
      if is_subscribed == 'True':
        users = User.objects.filter(**filters).filter(subscription__isnull=False, customer__isnull=False).filter((Q(username__icontains=text_search) | Q(first_name__icontains=text_search) | Q(last_name__icontains=text_search) | Q(email__icontains=text_search))).order_by('date_joined')
      else:
        users = User.objects.filter(**filters).filter((Q(username__icontains=text_search) | Q(first_name__icontains=text_search) | Q(last_name__icontains=text_search) | Q(email__icontains=text_search))).order_by('date_joined')

  paginator = Paginator(users, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'users.html', context)


@staff_member_required(login_url='login')
def manage_user(request, pk):
  try:
    user = User.objects.get(pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no user to manage.")
    return redirect('users')
  
  form = ManageUserForm()
  if request.method == 'POST':
    form = ManageUserForm(request.POST)
    if form.is_valid():
      form.save()
    else:
      print(form.errors)
  
  context = {'user': user, 'form': form}
  return render(request, 'manage_user.html', context)
