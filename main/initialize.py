from django.contrib.auth.models import Group, Permission
from pcr.models import ThermalCyclerProtocol


# Manager permissions
change_user = Permission.objects.get(codename='change_user')

change_profile = Permission.objects.get(codename="change_profile")
view_profile = Permission.objects.get(codename="view_profile")


manager_permissions = [change_user, change_profile, view_profile]

technician_permissions = [change_profile, view_profile]

incoming_permissions = [change_profile, view_profile]


def create_incoming_group():
  name = 'Incoming'
  if not Group.objects.filter(name=name).exists():
    group = Group.objects.create(name=name)
    group.permissions.set(incoming_permissions)
    print('group: incoming created')


def create_technician_group():
  name = 'Technician'
  if not Group.objects.filter(name=name).exists():
    group = Group.objects.create(name=name)
    group.permissions.set(technician_permissions)
    print('group: technician created')


def create_manager_group():
  name = 'Manager'
  if not Group.objects.filter(name=name).exists():
    group = Group.objects.create(name=name)
    group.permissions.set(manager_permissions)
    print('group: manager created')


# according to https://www.sigmaaldrich.com/US/en/technical-documents/protocol/genomics/pcr/standard-pcr
def create_basic_pcr_protocol():
  ThermalCyclerProtocol.objects.create(
    name = "Basic Thermal Cycling Protocol",
    denature_temp = 94.00,
    denature_duration = 60,
    anneal_temp = 55.00,
    anneal_duration = 120,
    extension_temp = 72,
    extension_duration = 180,
    number_of_cycles = 30,
  )