from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ..models.inventory import Reagent, Tube, Plate, Gel, Ladder, Dye
from ..models.assay import Assay
from ..models.batch import Batch
from ..models.pcr import Process


# **INVENTORY PARTIALS** #
@login_required(login_url='login')
def ladders_display(request):
  user = request.user
  ladders = Ladder.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(ladders, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/ladders_display.html', context)


@login_required(login_url='login')
def dyes_display(request):
  user = request.user
  dyes = Dye.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(dyes, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/dyes_display.html', context)


@login_required(login_url='login')
def plates_display(request):
  user = request.user
  plates = Plate.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(plates, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/plates_display.html', context)


@login_required(login_url='login')
def gels_display(request):
  user = request.user
  gels = Gel.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(gels, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/gels_display.html', context)


@login_required(login_url='login')
def tubes_display(request):
  user = request.user
  tubes = Tube.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(tubes, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/tubes_display.html', context)


@login_required(login_url='login')
def reagents_display(request):
  user = request.user
  reagents = Reagent.objects.filter(user=user).order_by('threshold_diff')

  paginator = Paginator(reagents, 3)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj}
  return render(request, 'dashboard/reagents_display.html', context)
# **INVENTORY PARTIALS** #


# **REPORT VIEWS** #
@login_required(login_url='login')
def inventory_report(request):
 
  context = {}
  return render(request, 'dashboard/inventory_dashboard.html', context)
# **REPORT VIEWS** #