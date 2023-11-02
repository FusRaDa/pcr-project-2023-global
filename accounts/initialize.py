from pcr.models import *

# according to https://www.sigmaaldrich.com/US/en/technical-documents/protocol/genomics/pcr/standard-pcr
def create_basic_pcr_protocol(user):
  ThermalCyclerProtocol.objects.create(
    user = user,
    name = "Basic Thermal Cycling Protocol",
    denature_temp = 94.00,
    denature_duration = 60,
    anneal_temp = 55.00,
    anneal_duration = 120,
    extension_temp = 72,
    extension_duration = 180,
    number_of_cycles = 30,
  )


def create_reagents(user):

  Reagent.objects.create(
    user = user,
    name = "DEPC Water",
    lot_number = "LOT_NUMBER_01",
    catalog_number = "CATALOG_NUMBER_01",
    storage_location = "STORAGE_LOCATION",
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.LITER,
  )

  Reagent.objects.create(
    user = user,
    name = "C.bovis F-primer",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    storage_location = "STORAGE_LOCATION",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  Reagent.objects.create(
    user = user,
    name = "C.bovis R-primer",
    lot_number = "LOT_NUMBER_03",
    catalog_number = "CATALOG_NUMBER_03",
    storage_location = "STORAGE_LOCATION",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  Reagent.objects.create(
    user = user,
    name = "Helico generic F-primer",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    storage_location = "STORAGE_LOCATION",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  Reagent.objects.create(
    user = user,
    name = "Helico generic F-primer",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    storage_location = "STORAGE_LOCATION",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  Reagent.objects.create(
    user = user,
    name = "Qiagen Multiplex PCR Master Mix",
    lot_number = "LOT_NUMBER_04",
    catalog_number = "CATALOG_NUMBER_04",
    storage_location = "STORAGE_LOCATION",
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.MILLILITER,
    stock_concentration = 2,
    unit_concentration = Reagent.ConcentrationUnits.X,
  )

def create_flourescence(user):

  Flourescence.objects.create(
    user = user,
    name = "TEX",
  )

  Flourescence.objects.create(
    user = user,
    name = "FAM",
  )

def create_controls(user):

  Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 1000c"
  )

  Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 100c"
  )

  Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 10c"
  )

  Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 1c"
  )

  Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "NegCtrl Water"
  )


# def create_assay_dna(user):
#   Reagent