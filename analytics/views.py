from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import datetime
import json
from django.db.models import Q
from django.core.paginator import Paginator

from users.models import User
from .models import LoginList, LoginAction
from .forms import SearchUserForm

# Create your views here.
@staff_member_required(login_url='login')
def dashboard(request):
  user_count = User.objects.count()
  sub_count = User.objects.filter(subscription__isnull=False, customer__isnull=False).count()
  login_list = LoginList.objects.all().order_by('-date')[:30][::-1] # latest thirty rows

  dates = []
  logins = []
  for val in login_list:
    dates.append(val.date_str)
    logins.append(val.logins)

  json_dates = json.dumps(dates)

  context = {'user_count': user_count, 'sub_count': sub_count, 'login_list': login_list, 'json_dates': json_dates, 'logins': logins}
  return render(request, 'dashboard.html', context)


@staff_member_required(login_url='login')
def users(request):
  users = User.objects.all().order_by('username')

  form = SearchUserForm()
  if request.method == 'GET':
    form = SearchUserForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      staff = form.cleaned_data['staff']
      active = form.cleaned_data['active']
      superuser = form.cleaned_data['superuser']
      can_review = form.cleaned_data['can_review']

      last_login_start = form.cleaned_data['last_login_start']
      last_login_end = form.cleaned_data['last_login_end']

      filters = {}
      if staff:
        filters['staff'] = staff
      if active:
        filters['active'] = active
      if superuser:
        filters['superuser'] = superuser
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

      users = User.objects.filter(**filters).filter((Q(username__icontains=text_search) | Q(first_name__icontains=text_search) | Q(last_name__icontains=text_search) | Q(email__icontains=text_search))).order_by('username')

    paginator = Paginator(users, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'users.html', context)
