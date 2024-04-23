from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F

from ..models.inventory import Reagent, Tube, Plate, Gel, Ladder, Dye
from ..models.assay import Assay, AssayCode, Control


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

  context = {'ladders': ladders[:5], 'is_low': is_low, 'is_expired': is_expired}
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

  context = {'dyes': dyes[:5], 'is_low': is_low, 'is_expired': is_expired}
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

  context = {'plates': plates[:5], 'is_low': is_low, 'is_expired': is_expired}
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

  context = {'gels': gels[:5], 'is_low': is_low, 'is_expired': is_expired}
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

  context = {'tubes': tubes[:5], 'is_low': is_low, 'is_expired': is_expired}
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

  context = {'reagents': reagents[:5], 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/reagents_display.html', context)
# **INVENTORY PARTIALS** #

# **TESTS PARTIALS** #
@login_required(login_url='login')
def controls_display(request):
  user = request.user
  controls = Control.objects.filter(user=user).order_by('amount')

  is_low = False
  is_expired = False

  for control in controls:
    if control.amount <= 100:
      is_low = True
      break

  for control in controls:
    if control.is_expired or control.month_exp:
      is_expired = True
      break

  context = {'controls': controls[:10], 'is_low': is_low, 'is_expired': is_expired}
  return render(request, 'dashboard/controls_display.html', context)


@login_required(login_url='login')
def assays_chart(request):
  assays = Assay.objects.filter(user=request.user).order_by('name')

  names = []
  numbers = []
  assays_dict = {}

  for assay in assays:
    names.append(assay.name)
    numbers.append(assay.sample_set.count())
    url = reverse('edit_assay', kwargs={'pk': assay.pk})
    assays_dict[assay.name] = url

  context = {'names': names, 'numbers': numbers, 'assays_dict': assays_dict}
  return render(request, 'dashboard/assays_chart.html', context)


@login_required(login_url='login')
def panels_chart(request):
  assays_codes = AssayCode.objects.filter(user=request.user).order_by('name')

  names = []
  numbers = []
  assays_dict = {}

  for code in assays_codes:
    names.append(code.name)
    numbers.append(code.batch_set.count())
    url = reverse('edit_assay_code', kwargs={'pk': code.pk})
    assays_dict[code.name] = url

  context = {'names': names, 'numbers': numbers, 'assays_dict': assays_dict}
  return render(request, 'dashboard/panels_chart.html', context)
# **TESTS PARTIALS** #

# **REPORT VIEWS** #
@login_required(login_url='login')
def inventory_report(request):
  
  ladders = Ladder.objects.filter(user=request.user)
  dyes = Dye.objects.filter(user=request.user)
  plates = Plate.objects.filter(user=request.user)
  gels = Gel.objects.filter(user=request.user)
  tubes = Tube.objects.filter(user=request.user)
  reagents = Reagent.objects.filter(user=request.user)
  controls = Control.objects.filter(user=request.user)

  ladders_warn = False
  dyes_warn = False
  plates_warn = False
  gels_warn = False
  tubes_warn = False
  reagents_warn = False
  controls_warn = False

  for ladder in ladders:
    if ladder.is_expired or ladder.month_exp or (ladder.threshold_diff is not None and ladder.threshold_diff <= 0):
      ladders_warn = True
      break

  for dye in dyes:
    if dye.is_expired or dye.month_exp or (dye.threshold_diff is not None and dye.threshold_diff <= 0):
      dyes_warn = True
      break

  for plate in plates:
    if plate.is_expired or plate.month_exp or (plate.threshold_diff is not None and plate.threshold_diff <= 0):
      plates_warn = True
      break

  for gel in gels:
    if gel.is_expired or gel.month_exp or (gel.threshold_diff is not None and gel.threshold_diff <= 0):
      gels_warn = True
      break

  for tube in tubes:
    if tube.is_expired or tube.month_exp or (tube.threshold_diff is not None and tube.threshold_diff <= 0):
      tubes_warn = True
      break

  for reagent in reagents:
    if reagent.is_expired or reagent.month_exp or (reagent.threshold_diff is not None and reagent.threshold_diff <= 0):
      reagents_warn = True
      break

  for control in controls:
    if control.is_expired or control.month_exp or control.amount <= 100:
      controls_warn = True
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

    if controls_warn:
      message += "controls, "

    message += "require your attention!"

  context = { 'message': message}
  return render(request, 'dashboard/inventory_dashboard.html', context)
# **REPORT VIEWS** #