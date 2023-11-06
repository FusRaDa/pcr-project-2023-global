from pcr.models import *

def create_presets(user):

  # according to https://www.sigmaaldrich.com/US/en/technical-documents/protocol/genomics/pcr/standard-pcr
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

  # Reagents for c.bovis and helico
  water = Reagent.objects.create(
    user = user,
    name = "DEPC Water",
    lot_number = "LOT_NUMBER_01",
    catalog_number = "CATALOG_NUMBER_01",
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.LITER,
  )

  cbov_fprimer = Reagent.objects.create(
    user = user,
    name = "C.bovis F-primer",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  cbov_rprimer = Reagent.objects.create(
    user = user,
    name = "C.bovis R-primer",
    lot_number = "LOT_NUMBER_03",
    catalog_number = "CATALOG_NUMBER_03",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  helico_fprimer = Reagent.objects.create(
    user = user,
    name = "Helico generic F-primer",
    lot_number = "LOT_NUMBER_04",
    catalog_number = "CATALOG_NUMBER_04",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  helico_rprimer = Reagent.objects.create(
    user = user,
    name = "Helico generic R-primer",
    lot_number = "LOT_NUMBER_05",
    catalog_number = "CATALOG_NUMBER_05",
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  q_multiplex = Reagent.objects.create(
    user = user,
    name = "Qiagen Multiplex PCR Master Mix",
    lot_number = "LOT_NUMBER_06",
    catalog_number = "CATALOG_NUMBER_06",
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.MILLILITER,
    stock_concentration = 2,
    unit_concentration = Reagent.ConcentrationUnits.X,
  )

  # Flourescence for cbovis and helico
  tex = Flourescence.objects.create(
    user = user,
    name = "TEX",
  )

  fam = Flourescence.objects.create(
    user = user,
    name = "FAM",
  )

  # Controls for cbovis and helico
  bact3 = Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 1000c"
  )

  bact2 = Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 100c"
  )

  bact1 = Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 10c"
  )

  bact0 = Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "Bact-PC 1c"
  )

  negctrl = Control.objects.create(
    user = user,
    lot_number = "LOT_NUMBER",
    name = "NegCtrl Water"
  )

  cbovis = Assay.objects.create(
     user = user,
     name = "C.Bovis",
     type = Assay.Types.DNA,
  )

  helico = Assay.objects.create(
    user = user,
    name = "Helico",
    type = Assay.Types.DNA

  ) 

  cbovis.controls.add(bact3, bact2, bact1, bact0, negctrl)
  cbovis.fluorescence.add(tex)
  cbovis.reagents.add(water, cbov_fprimer, cbov_rprimer, q_multiplex)

  helico.controls.add(bact3, negctrl)
  helico.fluorescence.add(fam)
  helico.reagents.add(water, helico_fprimer, helico_rprimer, q_multiplex)

  cbovis_assay = AssayCode.objects.create(
    user = user,
    name = "CBOV312",
  )

  helico_assay = AssayCode.objects.create(
    user = user,
    name = "HELI996",
  )

  cbov_heli = AssayCode.objects.create(
    user = user,
    name = "CBOV_HELI34",
  )

  cbovis_assay.assays.add(cbovis)
  helico_assay.assays.add(helico)
  cbov_heli.assays.add(cbovis, helico)
