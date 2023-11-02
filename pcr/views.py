from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group, User

# Create your views here.

@login_required(login_url='login')
def batches(request):

  context = []
  return render(request, "batches.html", context)


