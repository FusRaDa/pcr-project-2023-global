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
  

  # **INVENTORY SECTION** #
  plate96 = Plate.objects.create(
    user = user,
    name = "Generic 96-well plates",
    lot_number = "LOT_NUMBER_01",
    catalog_number = "CATALOG_NUMBER_01",
    size = Plate.Sizes.NINETY_SIX,
    amount = 50,
  )

  plate48 = Plate.objects.create(
    user = user,
    name = "Generic 48-well plates",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    size = Plate.Sizes.FOURTY_EIGHT,
    amount = 50,
  )

  plate384 = Plate.objects.create(
    user = user,
    name = "Generic 384-well plates",
    lot_number = "LOT_NUMBER_03",
    catalog_number = "CATALOG_NUMBER_03",
    size = Plate.Sizes.THREE_HUNDRED_EIGHTY_FOUR,
    amount = 50,
  )

  tubes1 = Tube.objects.create(
    user = user,
    name = "Generic 1.7ml Tubes",
    lot_number = "LOT_NUMBER_01",
    catalog_number = "CATALOG_NUMBER_01",
    amount = 500,
  )

  tubes2 = Tube.objects.create(
    user = user,
    name = "Generic 2ml w/ spin column",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    amount = 500,
  )

  tubes3 = Tube.objects.create(
    user = user,
    name = "Generic 2ml open column",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    amount = 500,
  )

  # Reagents for Extraction (dna tissue and dna fecal)
  proteinase_k = Reagent.objects.create(
    user = user, 
    name = "Proteinase K",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_07",
    catalog_number = "CATALOG_NUMBER_07",
    usage = Reagent.Usages.EXTRACTION,
    volume = 500.00,
    unit_volue = Reagent.VolumeUnits.MICROLITER,
  )

  al_buffer = Reagent.objects.create(
    user = user, 
    name = "AL Buffer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_08",
    catalog_number = "CATALOG_NUMBER_08",
    usage = Reagent.Usages.EXTRACTION,
    volume = 50.00,
    unit_volue = Reagent.VolumeUnits.MILLILITER,
  )

  ethanol = Reagent.objects.create(
    user = user, 
    name = "Ethanol",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_09",
    catalog_number = "CATALOG_NUMBER_09",
    usage = Reagent.Usages.EXTRACTION,
    volume = 1.00,
    unit_volue = Reagent.VolumeUnits.LITER,
  )

  aw1_buffer = Reagent.objects.create(
    user = user, 
    name = "AW1 Buffer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_10",
    catalog_number = "CATALOG_NUMBER_10",
    usage = Reagent.Usages.EXTRACTION,
    volume = 100.00,
    unit_volue = Reagent.VolumeUnits.MILLILITER,
  )

  aw2_buffer = Reagent.objects.create(
    user = user, 
    name = "AW2 Buffer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_11",
    catalog_number = "CATALOG_NUMBER_11",
    usage = Reagent.Usages.EXTRACTION,
    volume = 100.00,
    unit_volue = Reagent.VolumeUnits.MILLILITER,
  )

  ae_buffer = Reagent.objects.create(
    user = user, 
    name = "AE Buffer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_12",
    catalog_number = "CATALOG_NUMBER_12",
    usage = Reagent.Usages.EXTRACTION,
    volume = 50.00,
    unit_volue = Reagent.VolumeUnits.MILLILITER,
  )

  atl_buffer = Reagent.objects.create(
    user = user, 
    name = "ATL Buffer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_13",
    catalog_number = "CATALOG_NUMBER_13",
    usage = Reagent.Usages.EXTRACTION,
    volume = 50.00,
    unit_volue = Reagent.VolumeUnits.MILLILITER,
  )

  # Reagents for PCR (c.bovis and helico)
  water = Reagent.objects.create(
    user = user,
    name = "DEPC Water",
    brand = "BRAND", 
    lot_number = "LOT_NUMBER_01",
    catalog_number = "CATALOG_NUMBER_01",
    usage = Reagent.Usages.PCR,
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.LITER,
  )

  cbov_fprimer = Reagent.objects.create(
    user = user,
    name = "C.bovis F-primer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_02",
    catalog_number = "CATALOG_NUMBER_02",
    usage = Reagent.Usages.PCR,
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 20,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  cbov_rprimer = Reagent.objects.create(
    user = user,
    name = "C.bovis R-primer",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_03",
    catalog_number = "CATALOG_NUMBER_03",
    usage = Reagent.Usages.PCR,
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 20,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  helico_f_r_primer = Reagent.objects.create(
    user = user,
    name = "Helico generic F+R-primer",
    brand = "BRAND", 
    lot_number = "LOT_NUMBER_04",
    catalog_number = "CATALOG_NUMBER_04",
    usage = Reagent.Usages.PCR,
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  helico_pprimer = Reagent.objects.create(
    user = user,
    name = "Helico generic P-primer",
    brand = "BRAND", 
    lot_number = "LOT_NUMBER_05",
    catalog_number = "CATALOG_NUMBER_05",
    usage = Reagent.Usages.PCR,
    volume = 100.00,
    unit_volume = Reagent.VolumeUnits.MICROLITER,
    stock_concentration = 10,
    unit_concentration = Reagent.ConcentrationUnits.MICROMOLES,
  )

  i_taq = Reagent.objects.create(
    user = user,
    name = "iTaq Universal Probes Supermix",
    brand = "BRAND",
    lot_number = "LOT_NUMBER_06",
    catalog_number = "CATALOG_NUMBER_06",
    usage = Reagent.Usages.PCR,
    volume = 1.00,
    unit_volume = Reagent.VolumeUnits.MILLILITER,
    stock_concentration = 2,
    unit_concentration = Reagent.ConcentrationUnits.X,
  )
  # **INVENTORY SECTION** #


  # **EXTRACTION SECTION** #
  dna_ext_tissue = ExtractionProtocol.objects.create(
    user = user,
    name = "DNA Extraction - Tissue",
    type = ExtractionProtocol.Types.DNA,
  )

  dna_ext_tissue.tubes.add(tubes1, tubes2, tubes3)
  dna_ext_tissue.reagents.add(proteinase_k, al_buffer, ethanol, aw1_buffer, aw2_buffer, ae_buffer)

  dna_ext_fecal = ExtractionProtocol.objects.create(
    user = user,
    name = "DNA Extraction - Fecal",
    type = ExtractionProtocol.Types.DNA,
  )

  dna_ext_fecal.tubes.add(tubes1, tubes2, tubes3)
  dna_ext_fecal.reagents.add(proteinase_k, al_buffer, ethanol, aw1_buffer, aw2_buffer, ae_buffer, atl_buffer)
  # **EXTRACTION SECTION** #

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
    name = "Bact-PC 1000c",
    lot_number = "LOT_NUMBER",
    amount = 100.00,
  )

  bact2 = Control.objects.create(
    user = user,
    name = "Bact-PC 100c",
    lot_number = "LOT_NUMBER",
    amount = 100.00,
  )

  bact1 = Control.objects.create(
    user = user,
    name = "Bact-PC 10c",
    lot_number = "LOT_NUMBER",
    amount = 100.00,
  )

  bact0 = Control.objects.create(
    user = user,
    name = "Bact-PC 1c",
    lot_number = "LOT_NUMBER",
    amount = 100.00,
  )

  negctrl = Control.objects.create(
    user = user,
    name = "NegCtrl Water",
    lot_number = "LOT_NUMBER",
    amount = 100.00,
  )

  cbovis_assay = Assay.objects.create(
     user = user,
     name = "C.Bovis",
     type = Assay.Types.DNA,
  )

  helico_assay = Assay.objects.create(
    user = user,
    name = "Helico",
    type = Assay.Types.DNA
  ) 

  cbovis_assay.controls.add(bact3, bact2, bact1, bact0, negctrl)
  cbovis_assay.fluorescence.add(tex)
  cbovis_assay.reagents.add(water, cbov_fprimer, cbov_rprimer, i_taq)

  helico_assay.controls.add(bact3, negctrl)
  helico_assay.fluorescence.add(fam)
  helico_assay.reagents.add(water, helico_f_r_primer, helico_pprimer, i_taq)

  ReagentAssay.objects.create(
    reagent = water, 
    assay = cbovis_assay,
    amount_per_sample = 3.90,
  )

  ReagentAssay.objects.create(
    reagent = cbov_fprimer, 
    assay = cbovis_assay,
    amount_per_sample = 0.90,
  )

  ReagentAssay.objects.create(
    reagent = cbov_rprimer, 
    assay = cbovis_assay,
    amount_per_sample = 0.20,
  )

  ReagentAssay.objects.create(
    reagent = i_taq, 
    assay = cbovis_assay,
    amount_per_sample = 10.00,
  )

  ReagentAssay.objects.create(
    reagent = water, 
    assay = helico_assay,
    amount_per_sample = 1.20,
  )

  ReagentAssay.objects.create(
    reagent = helico_f_r_primer, 
    assay = helico_assay,
    amount_per_sample = 0.60,
  )

  ReagentAssay.objects.create(
    reagent = helico_pprimer, 
    assay = helico_assay,
    amount_per_sample = 0.20,
  )

  ReagentAssay.objects.create(
    reagent = i_taq, 
    assay = helico_assay,
    amount_per_sample = 10.00,
  )

  cbovis_code = AssayCode.objects.create(
    user = user,
    name = "CBOV312",
  )

  helico_code = AssayCode.objects.create(
    user = user,
    name = "HELI996",
  )

  cbov_heli_code = AssayCode.objects.create(
    user = user,
    name = "CBOV_HELI34",
  )

  cbovis_code.assays.add(cbovis_assay)
  helico_code.assays.add(helico_assay)
  cbov_heli_code.assays.add(cbovis_assay, helico_assay)
