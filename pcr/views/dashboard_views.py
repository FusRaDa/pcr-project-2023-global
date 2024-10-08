from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F

from ..custom.functions import detect_inventory_usage, detect_mergeable_items

from ..models.inventory import Reagent, Tube, Plate, Gel, Ladder, Dye
from ..models.assay import Assay, AssayCode, Control
from ..models.batch import Batch
from ..models.pcr import Process


# **INVENTORY PARTIALS** #
@login_required(login_url='login')
def ladders_display(request):
  ladders = Ladder.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))

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
  dyes = Dye.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))
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
  plates = Plate.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))

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
  gels = Gel.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))

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
  tubes = Tube.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))

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
  reagents = Reagent.objects.filter(user=request.user).order_by(F('threshold_diff').asc(nulls_last=True))

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
  controls = Control.objects.filter(user=request.user).order_by('amount')

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

  names_assays = []
  numbers_assays = []
  assays_dict = {}

  for assay in assays:
    names_assays.append(assay.name)
    numbers_assays.append(assay.sample_set.count())
    url = reverse('edit_assay', kwargs={'pk': assay.pk})
    assays_dict[assay.name] = url

  context = {'names_assays': names_assays, 'numbers_assays': numbers_assays, 'assays_dict': assays_dict}
  return render(request, 'dashboard/assays_chart.html', context)


@login_required(login_url='login')
def panels_chart(request):
  assays_codes = AssayCode.objects.filter(user=request.user).order_by('name')

  names_codes = []
  numbers_codes = []
  assay_codes_dict = {}

  for code in assays_codes:
    names_codes.append(code.name)
    numbers_codes.append(code.batch_set.count())
    url = reverse('edit_assay_code', kwargs={'pk': code.pk})
    assay_codes_dict[code.name] = url

  context = {'names_codes': names_codes, 'numbers_codes': numbers_codes, 'assay_codes_dict': assay_codes_dict}
  return render(request, 'dashboard/panels_chart.html', context)
# **TESTS PARTIALS** #


# **PROCESS & BATCH** #
@login_required(login_url='login')
def batches_display(request):
  batches = Batch.objects.filter(user=request.user).order_by('-date_created')

  in_que = False

  for batch in batches:
    if batch.is_extracted == False:
      in_que = True
      break

  context = {'batches': batches[:10], 'in_que': in_que}
  return render(request, 'dashboard/batches_display.html', context)


@login_required(login_url='login')
def processes_display(request):
  processes = Process.objects.filter(user=request.user).order_by('-date_processed')

  in_que = False

  for process in processes:
    if process.is_processed == False:
      in_que = True
      break

  context = {'processes': processes[:10], 'in_que': in_que}
  return render(request, 'dashboard/processes_display.html', context)
# **PROCESS & BATCH** #


# **REPORT/DASHBOARD VIEWS** #
@login_required(login_url='login')
def inventory_report(request):
  ladders = Ladder.objects.filter(user=request.user).order_by('catalog_number')
  dyes = Dye.objects.filter(user=request.user).order_by('catalog_number')
  plates = Plate.objects.filter(user=request.user).order_by('catalog_number')
  gels = Gel.objects.filter(user=request.user).order_by('catalog_number')
  tubes = Tube.objects.filter(user=request.user).order_by('catalog_number')
  reagents = Reagent.objects.filter(user=request.user).order_by('catalog_number')
  controls = Control.objects.filter(user=request.user).order_by('catalog_number')

  inventory_message = detect_inventory_usage(
    ladders=ladders,
    dyes=dyes,
    plates=plates,
    gels=gels,
    tubes=tubes,
    reagents=reagents,
    controls=controls,
  )

  mergeable_message = detect_mergeable_items(
    ladders=ladders,
    dyes=dyes,
    plates=plates,
    gels=gels,
    tubes=tubes,
    reagents=reagents,
    controls=controls,
  )

  context = { 'inventory_message': inventory_message, 'mergeable_message': mergeable_message}
  return render(request, 'dashboard/inventory_dashboard.html', context)
# **REPORT VIEWS** #