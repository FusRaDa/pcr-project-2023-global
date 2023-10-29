from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('accounts')
    else:
      return view_func(request, *args, **kwargs)
  return wrapper_func


def manager_only(view_func):
  def wrapper_function(request, *args, **kwargs):
    group = None
    if request.user.groups.exists():
      group = request.user.groups.all()[0].name
      
      if group == 'Manager':
        return view_func(request, *args, **kwargs)
      else:
        return redirect('accounts')
        
  return wrapper_function


def lab_access(view_func):
  def wrapper_function(request, *args, **kwargs):
    group = None
    if request.user.groups.exists():
      group = request.user.groups.all()[0].name
      
      if group == 'Manager' or group == 'Technician':
        return view_func(request, *args, **kwargs)
      else:
        return redirect('profile')
        
  return wrapper_function