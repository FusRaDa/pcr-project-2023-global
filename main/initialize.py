from pcr.models import ThermalCyclerProtocol

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