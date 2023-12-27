from django.test import TestCase

from pcr.models.pcr import ThermalCyclerProtocol
from pcr.models.inventory import Tube, Plate, Reagent, Location
from pcr.models.extraction import ExtractionProtocol
from pcr.models.assay import Assay, AssayCode, Control, Fluorescence

from users.models import User


class ThermalCyclerProtocolTestCase(TestCase):

  def setup_thermalcyclerprotocols(self):
    user = User.objects.get(username='fusrada1')

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
      number_of_cycles = 30)


class LocationTestCase(TestCase):
    
  def setup_locations(self):
    user = User.objects.get(username='fusrada1')

    Location.objects.create(user=user, name = "Location 1")
    Location.objects.create(user=user, name="Location 2")
    Location.objects.create(user=user, name="Location 3")


class PlateTestCase(TestCase):
    
  def setup_plates(self):
    user = User.objects.get(username='fusrada1')

    location1 = Location.objects.get(user=user, name="Location 1")

    plate1 = Plate.objects.create(
      user = user,
      name = "Generic 96-well plates",
      lot_number = "LOT_NUMBER_01",
      catalog_number = "CATALOG_NUMBER_01",
      size = Plate.Sizes.NINETY_SIX,
      amount = 50)
    plate1.location.add(location1)

    plate2 = Plate.objects.create(
      user = user,
      name = "Generic 48-well plates",
      lot_number = "LOT_NUMBER_02",
      catalog_number = "CATALOG_NUMBER_02",
      size = Plate.Sizes.FOURTY_EIGHT,
      amount = 50)
    plate2.location.add(location1)

    plate3 = Plate.objects.create(
      user = user,
      name = "Generic 384-well plates",
      lot_number = "LOT_NUMBER_03",
      catalog_number = "CATALOG_NUMBER_03",
      size = Plate.Sizes.THREE_HUNDRED_EIGHTY_FOUR,
      amount = 50)
    plate3.location.add(location1)


class TubeTestCase(TestCase):
  def setup_tubes(self):
    user = User.objects.get(username='fusrada1')

    location1 = Location.objects.get(user=user, name="Location 1")

    tubes1 = Tube.objects.create(
      user = user,
      name = "Generic 1.7ml Tubes",
      lot_number = "LOT_NUMBER_01",
      catalog_number = "CATALOG_NUMBER_01",
      amount = 500)
    tubes1.location.add(location1)

    tubes2 = Tube.objects.create(
      user = user,
      name = "Generic 2ml w/ spin column",
      lot_number = "LOT_NUMBER_02",
      catalog_number = "CATALOG_NUMBER_02",
      amount = 500)
    tubes2.location.add(location1)

    tubes3 = Tube.objects.create(
      user = user,
      name = "Generic 2ml open column",
      lot_number = "LOT_NUMBER_03",
      catalog_number = "CATALOG_NUMBER_03",
      amount = 500)
    tubes3.location.add(location1)


class ReagentTestCase(TestCase):
  
  def setup_reagents(self):
    user = User.objects.get(username='fusrada1')

    location2 = Location.objects.get(user=user, name="Location 2")
    location3 = Location.objects.get(user=user, name="Location 3")

    proteinase_k = Reagent.objects.create(
      user = user, 
      name = "Proteinase K",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_07",
      catalog_number = "CATALOG_NUMBER_07",
      usage = Reagent.Usages.EXTRACTION,
      volume = 500.00,
      unit_volume = Reagent.VolumeUnits.MICROLITER)
    proteinase_k.location.add(location2)

    al_buffer = Reagent.objects.create(
      user = user, 
      name = "AL Buffer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_08",
      catalog_number = "CATALOG_NUMBER_08",
      usage = Reagent.Usages.EXTRACTION,
      volume = 50.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER)

    al_buffer.location.add(location2)

    ethanol = Reagent.objects.create(
      user = user, 
      name = "Ethanol",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_09",
      catalog_number = "CATALOG_NUMBER_09",
      usage = Reagent.Usages.EXTRACTION,
      volume = 1.00,
      unit_volume = Reagent.VolumeUnits.LITER)
    ethanol.location.add(location2)

    aw1_buffer = Reagent.objects.create(
      user = user, 
      name = "AW1 Buffer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_10",
      catalog_number = "CATALOG_NUMBER_10",
      usage = Reagent.Usages.EXTRACTION,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER)
    aw1_buffer.location.add(location2)

    aw2_buffer = Reagent.objects.create(
      user = user, 
      name = "AW2 Buffer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_11",
      catalog_number = "CATALOG_NUMBER_11",
      usage = Reagent.Usages.EXTRACTION,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER)
    aw2_buffer.location.add(location2)

    ae_buffer = Reagent.objects.create(
      user = user, 
      name = "AE Buffer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_12",
      catalog_number = "CATALOG_NUMBER_12",
      usage = Reagent.Usages.EXTRACTION,
      volume = 50.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER)
    ae_buffer.location.add(location2)

    atl_buffer = Reagent.objects.create(
      user = user, 
      name = "ATL Buffer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_13",
      catalog_number = "CATALOG_NUMBER_13",
      usage = Reagent.Usages.EXTRACTION,
      volume = 50.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER)
    atl_buffer.location.add(location2)

    water = Reagent.objects.create(
      user = user,
      name = "DEPC Water",
      brand = "BRAND", 
      lot_number = "LOT_NUMBER_01",
      catalog_number = "CATALOG_NUMBER_01",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.WATER,
      volume = 1.00,
      unit_volume = Reagent.VolumeUnits.LITER)
    water.location.add(location3)

    cbov_frprimer = Reagent.objects.create(
      user = user,
      name = "C.bovis F+R-primer",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_02",
      catalog_number = "CATALOG_NUMBER_02",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.GENERAL,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MICROLITER,
      stock_concentration = 20,
      unit_concentration = Reagent.ConcentrationUnits.MICROMOLES)
    cbov_frprimer.location.add(location3)

    cbov_pprimer = Reagent.objects.create(
      user = user,
      name = "C.bovis probe",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_03",
      catalog_number = "CATALOG_NUMBER_03",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.GENERAL,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MICROLITER,
      stock_concentration = 20,
      unit_concentration = Reagent.ConcentrationUnits.MICROMOLES)
    cbov_pprimer.location.add(location3)

    helico_frprimer = Reagent.objects.create(
      user = user,
      name = "Helico generic F+R-primer",
      brand = "BRAND", 
      lot_number = "LOT_NUMBER_04",
      catalog_number = "CATALOG_NUMBER_04",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.GENERAL,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MICROLITER,
      stock_concentration = 10,
      unit_concentration = Reagent.ConcentrationUnits.MICROMOLES)
    helico_frprimer.location.add(location3)

    helico_pprimer = Reagent.objects.create(
      user = user,
      name = "Helico generic probe",
      brand = "BRAND", 
      lot_number = "LOT_NUMBER_05",
      catalog_number = "CATALOG_NUMBER_05",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.GENERAL,
      volume = 100.00,
      unit_volume = Reagent.VolumeUnits.MICROLITER,
      stock_concentration = 10,
      unit_concentration = Reagent.ConcentrationUnits.MICROMOLES)
    helico_pprimer.location.add(location3)

    i_taq = Reagent.objects.create(
      user = user,
      name = "iTaq Universal Probes Supermix",
      brand = "BRAND",
      lot_number = "LOT_NUMBER_06",
      catalog_number = "CATALOG_NUMBER_06",
      usage = Reagent.Usages.PCR,
      pcr_reagent = Reagent.PCRReagent.POLYMERASE,
      volume = 1.00,
      unit_volume = Reagent.VolumeUnits.MILLILITER,
      stock_concentration = 5,
      unit_concentration = Reagent.ConcentrationUnits.UNITS)
    i_taq.location.add(location3)



class ExtractionProtocolTestCase(TestCase):
    
  def setup_extractionprotocols(self):
    user = User.objects.get(username='fusrada1')

    tubes1 = Tube.objects.get(user = user, name = "Generic 1.7ml Tubes")
    tubes2 = Tube.objects.get(user=user, name="Generic 2ml w/ spin column")
    tubes3 = Tube.objects.get(user=user, name="Generic 2ml open column")

    proteinase_k = Reagent.objects.get(user=user, name="Proteinase K")
    al_buffer = Reagent.objects.get(user=user, name="AL Buffer")
    ethanol = Reagent.objects.get(user=user, name="Ethanol")
    aw1_buffer = Reagent.objects.get(user=user, name="AW1 Buffer")
    aw2_buffer = Reagent.objects.get(user=user, name="AW2 Buffer")
    ae_buffer = Reagent.objects.get(user=user, name="AE Buffer")
    atl_buffer = Reagent.objects.get(user = user, name = "ATL Buffer")

    dna_ext_tissue = ExtractionProtocol.objects.create(
      user = user,
      name = "DNA Extraction - Tissue",
      type = ExtractionProtocol.Types.DNA,
      doc_url = "https://www.qiagen.com/us/resources/resourcedetail?id=68f29296-5a9f-40fa-8b3d-1c148d0b3030&lang=en",
    )
    dna_ext_tissue.tubes.add(tubes1, tubes2, tubes3)
    dna_ext_tissue.reagents.add(proteinase_k, al_buffer, ethanol, aw1_buffer, aw2_buffer, ae_buffer)

    dna_ext_fecal = ExtractionProtocol.objects.create(
      user = user,
      name = "DNA Extraction - Fecal",
      type = ExtractionProtocol.Types.DNA,
      doc_url = "https://www.qiagen.com/us/resources/resourcedetail?id=2a3f2c0b-2e8a-49fd-b442-829108ae1a4a&lang=en",
    )
    dna_ext_fecal.tubes.add(tubes1, tubes2, tubes3)
    dna_ext_fecal.reagents.add(proteinase_k, al_buffer, ethanol, aw1_buffer, aw2_buffer, ae_buffer, atl_buffer)
    

class FluorescenceTestCase(TestCase):
    
  def setup_fluorescences(self):
    user = User.objects.get(username='fusrada1')

    Fluorescence.objects.create(user=user, name="TEX")
    Fluorescence.objects.create(user=user, name="FAM")


class ControlTestCase(TestCase):
    
  def setup_controls(self):
    user = User.objects.get(username='fusrada1')

    location3 = Location.objects.get(user=user, name="Location 3")

    bact3 = Control.objects.create(
      user = user,
      name = "Bact-PC 1000c",
      lot_number = "LOT_NUMBER_01",
      amount = 100.00)
    bact3.location.add(location3)

    bact2 = Control.objects.create(
      user = user,
      name = "Bact-PC 100c",
      lot_number = "LOT_NUMBER_02",
      amount = 100.00)
    bact2.location.add(location3)

    bact1 = Control.objects.create(
      user = user,
      name = "Bact-PC 10c",
      lot_number = "LOT_NUMBER_03",
      amount = 100.00)
    bact1.location.add(location3)

    bact0 = Control.objects.create(
      user = user,
      name = "Bact-PC 1c",
      lot_number = "LOT_NUMBER_04",
      amount = 100.00)
    bact0.location.add(location3)

    negctrl = Control.objects.create(
      user = user,
      name = "NegCtrl Water",
      lot_number = "LOT_NUMBER_05",
      is_negative_ctrl = True,
      amount = 100.00)
    negctrl.location.add(location3)


class AssayTestCase(TestCase):
  
  def setup_assays(self):
    user = User.objects.get(username='fusrada1')

    tex = Fluorescence.objects.create(user=user, name="TEX")
    fam = Fluorescence.objects.create(user=user, name="FAM")

    bact3 = Control.objects.get(user=user, name="Bact-PC 1000c")
    bact2 = Control.objects.get(user=user, name="Bact-PC 100c")
    bact1 = Control.objects.get(user=user, name="Bact-PC 10c")
    bact0 = Control.objects.get(user=user, name="Bact-PC 1c")
    negctrl = Control.objects.get(user=user, name="NegCtrl Water")

    water = Reagent.objects.get(user=user, name="DEPC Water")
    cbov_frprimer = Reagent.objects.get(user=user, name="C.bovis F+R-primer")
    cbov_pprimer = Reagent.objects.get(user=user, name="C.bovis probe")
    helico_frprimer = Reagent.objects.get(user=user, name="Helico generic F+R-primer")
    helico_pprimer = Reagent.objects.get(user=user, name="Helico generic probe")
    i_taq = Reagent.objects.get(user=user, name="iTaq Universal Probes Supermix")
    
    cbovis_assay = Assay.objects.create(
      user = user,
      name = "C.Bovis",
      method = Assay.Methods.PCR,
      type = Assay.Types.DNA,
      sample_volume = 5.00,
      reaction_volume = 20.00)

    helico_assay = Assay.objects.create(
      user = user,
      name = "Helico",
      method = Assay.Methods.qPCR,
      type = Assay.Types.DNA,
      sample_volume = 8.00,
      reaction_volume = 20.00) 

    cbovis_assay.controls.add(bact3, bact2, bact1, bact0, negctrl)
    cbovis_assay.fluorescence.add(tex)
    cbovis_assay.reagents.add(water, cbov_frprimer, cbov_pprimer, i_taq)

    helico_assay.controls.add(bact3, negctrl)
    helico_assay.fluorescence.add(fam)
    helico_assay.reagents.add(water, helico_frprimer, helico_pprimer, i_taq)


class AssayCodeTestCase(TestCase):
    
  def setup_assaycodes(self):
    user = User.objects.get(username='fusrada1')

    cbovis_assay = Assay.objects.get(user=user, name="C.Bovis")
    helico_assay = Assay.objects.get(user=user, name="Helico")

    cbovis_code = AssayCode.objects.create(user=user, name="CBOV312",)
    helico_code = AssayCode.objects.create(user=user, name="HELI996")
    cbov_heli_code = AssayCode.objects.create(user=user, name="CBOV_HELI34")

    cbovis_code.assays.add(cbovis_assay)
    helico_code.assays.add(helico_assay)
    cbov_heli_code.assays.add(cbovis_assay, helico_assay)