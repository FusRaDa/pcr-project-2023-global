from django.test import TestCase

from store.models.affiliates import Brand, Contact
from store.models.items import Tag, Kit, StorePlate, StoreReagent, StoreTube


class BrandTestCase(TestCase):
  def run():

    brand1 = Brand.objects.create(
      name = "BRAND1_COMPANY1",
      is_affiliated = True,
    )

    brand2 = Brand.objects.create(
      name = "BRAND2_COMPANY2",
      is_affiliated = False,
    )

    Contact.objects.create(
      brand = brand1,
      company = "COMPANY1",
      first_name = "CONTACT_FIRST_NAME1",
      last_name = "CONTACT_LAST_NAME1",
      email = "contactone@gmail.com",
      phone_number = "+13023435467"
    )

    Contact.objects.create(
      brand = brand2,
      company = "COMPANY2",
      first_name = "CONTACT_FIRST_NAME2",
      last_name = "CONTACT_LAST_NAME2",
      email = "contacttwo@gmail.com",
      phone_number = "+13453452244"
    )

    tag1 = Tag.objects.create(
      name = "TAG1"
    )

    tag2 = Tag.objects.create(
      name = "TAG2"
    )

    tag3 = Tag.objects.create(
      name = "TAG3"
    )

    # Kits for BRAND 1
    kit1 = Kit.objects.create(
      brand = brand1,
      name = "BRAND1_KIT1_T13",
      catalog_number = "CATALOG_NUMBER_1",
      price = 124.99,
    )
    kit1.tags.add(tag1, tag3)

    StoreReagent.objects.create(
      kit = kit1,
      name = "EXTRACTION_REAGENT_KIT1",
      usage = StoreReagent.Usages.EXTRACTION,
      volume = 300.00,
      unit_volume = StoreReagent.VolumeUnits.MILLILITER
    )

    StoreReagent.objects.create(
      kit = kit1,
      name = "PCR_GENERAL_REAGENT_KIT1",
      usage = StoreReagent.Usages.PCR,
      pcr_reagent = StoreReagent.PCRReagent.GENERAL,
      volume = 50.00,
      unit_volume = StoreReagent.VolumeUnits.MILLILITER,
      stock_concentration = 10,
      unit_concentration = StoreReagent.ConcentrationUnits.MICROMOLES
    )

    StoreTube.objects.create(
      kit = kit1,
      name = "TUBE1_KIT1",
      amount = 25,
    )

    kit2 = Kit.objects.create(
      brand = brand1,
      name = "BRAND1_KIT2_T2",
      catalog_number = "CATALOG_NUMBER_2",
      price = 74.99,
    )
    kit2.tags.add(tag2)

    StoreReagent.objects.create(
      kit = kit2,
      name = "REAGENT1_KIT2",
      usage = StoreReagent.Usages.EXTRACTION,
      volume = 1,
      unit_volume = StoreReagent.VolumeUnits.LITER,
    )

    StorePlate.objects.create(
      kit = kit2,
      name = "PLATE1_KIT2",
      size = StorePlate.Sizes.NINETY_SIX,
      amount = 25,
    )

    # Kits for BRAND 2
    kit3 = Kit.objects.create(
      brand = brand2,
      name = "BRAND2_KIT3_T12",
      catalog_number = "CATALOG_NUMBER_3",
      price = 124.99,
    )
    kit3.tags.add(tag1, tag2)

    StoreReagent.objects.create(
      kit = kit3,
      name = "REAGENT1_KIT3",
      usage = StoreReagent.Usages.PCR,
      pcr_reagent = StoreReagent.PCRReagent.WATER,
      volume = 5,
      unit_volume = StoreReagent.VolumeUnits.MILLILITER,
    )

    kit4 = Kit.objects.create(
      brand = brand2,
      name = "BRAND2_KIT_4_T3",
      catalog_number = "CATALOG_NUMBER_4",
      price = 74.99,
    )
    kit4.tags.add(tag3)

    StoreTube.objects.create(
      kit = kit4,
      name = "TUBE2_KIT4",
      amount = 50,
    )





