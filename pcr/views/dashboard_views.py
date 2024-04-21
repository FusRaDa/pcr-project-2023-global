from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F

from ..models.inventory import Reagent, Tube, Plate, Gel, Ladder, Dye
from ..models.assay import Assay
from ..models.batch import Batch
from ..models.pcr import Process


# **INVENTORY PARTIALS** #
@login_required(login_url='login')
def ladders_display(request):
  user = request.user
  ladders = Ladder.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for ladder in ladders:
    if ladder.threshold_diff is not None and ladder.threshold_diff <= 0:
      is_low = True
      break

  for ladder in ladders:
    if ladder.is_expired or ladder.month_exp:
      is_expired = True
      break
    
  paginator = Paginator(ladders, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/ladders_display.html', context)


@login_required(login_url='login')
def dyes_display(request):
  user = request.user
  dyes = Dye.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for dye in dyes:
    if dye.threshold_diff is not None and dye.threshold_diff <= 0:
      is_low = True
      break

  for dye in dyes:
    if dye.is_expired or dye.month_exp:
      is_expired = True
      break

  paginator = Paginator(dyes, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/dyes_display.html', context)


@login_required(login_url='login')
def plates_display(request):
  user = request.user
  plates = Plate.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for plate in plates:
    if plate.threshold_diff is not None and plate.threshold_diff <= 0:
      is_low = True
      break

  for plate in plates:
    if plate.is_expired or plate.month_exp:
      is_expired = True
      break

  paginator = Paginator(plates, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/plates_display.html', context)


@login_required(login_url='login')
def gels_display(request):
  user = request.user
  gels = Gel.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for gel in gels:
    if gel.threshold_diff is not None and gel.threshold_diff <= 0:
      is_low = True
      break

  for gel in gels:
    if gel.is_expired or gel.month_exp:
      is_expired = True
      break

  paginator = Paginator(gels, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/gels_display.html', context)


@login_required(login_url='login')
def tubes_display(request):
  user = request.user
  tubes = Tube.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for tube in tubes:
    if tube.threshold_diff is not None and tube.threshold_diff <= 0:
      is_low = True
      break

  for tube in tubes:
    if tube.is_expired or tube.month_exp:
      is_expired = True
      break

  paginator = Paginator(tubes, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/tubes_display.html', context)


@login_required(login_url='login')
def reagents_display(request):
  user = request.user
  reagents = Reagent.objects.filter(user=user).order_by(F('threshold_diff').asc(nulls_last=True))

  is_low = False
  is_expired = False

  for reagent in reagents:
    if reagent.threshold_diff is not None and reagent.threshold_diff <= 0:
      is_low = True
      break

  for reagent in reagents:
    if reagent.is_expired or reagent.month_exp:
      is_expired = True
      break

  paginator = Paginator(reagents, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/reagents_display.html', context)
# **INVENTORY PARTIALS** #


# **REPORT VIEWS** #
@login_required(login_url='login')
def inventory_report(request):
  
  ladders = Ladder.objects.filter(user=request.user)
  dyes = Dye.objects.filter(user=request.user)
  plates = Plate.objects.filter(user=request.user)
  gels = Gel.objects.filter(user=request.user)
  tubes = Tube.objects.filter(user=request.user)
  reagents = Reagent.objects.filter(user=request.user)

  ladders_warn = False
  dyes_warn = False
  plates_warn = False
  gels_warn = False
  tubes_warn = False
  reagents_warn = False

  for ladder in ladders:
    if ladder.is_expired or (ladder.threshold_diff is not None and ladder.threshold_diff <= 0):
      ladders_warn = True
      break

  for dye in dyes:
    if dye.is_expired or (dye.threshold_diff is not None and dye.threshold_diff <= 0):
      dyes_warn = True
      break

  for plate in plates:
    if plate.is_expired or (plate.threshold_diff is not None and plate.threshold_diff <= 0):
      plates_warn = True
      break

  for gel in gels:
    if gel.is_expired or (gel.threshold_diff is not None and gel.threshold_diff <= 0):
      gels_warn = True
      break

  for tube in tubes:
    if tube.is_expired or (tube.threshold_diff is not None and tube.threshold_diff <= 0):
      tubes_warn = True
      break

  for reagent in reagents:
    if reagent.is_expired or (reagent.threshold_diff is not None and reagent.threshold_diff <= 0):
      reagents_warn = True
      break

  message = None
  if ladders_warn or dyes_warn or plates_warn or gels_warn or tubes_warn or reagents_warn:
    message = "Inventory for "

    if ladders_warn:
      message += "ladders, "

    if dyes_warn:
      message += "dyes, "

    if plates_warn:
      message += "plates, "

    if gels_warn:
      message += "gels, "

    if tubes_warn:
      message += "tubes, "

    if reagents_warn:
      message += "reagents, "

    message += "require your attention!"

  context = { 'message': message}
  return render(request, 'dashboard/inventory_dashboard.html', context)
# **REPORT VIEWS** #