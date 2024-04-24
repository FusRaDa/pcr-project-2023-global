import random
import string
import csv
from django.core.files.storage import default_storage

from pcr.models.inventory import Tube, Plate, Reagent, Gel, Dye, Ladder


def generate_random_file_name(length):
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def generate_order_files(order, inputs):
  folder = 'orders/'

  brand_arr = []
  for kit in order.kits.all():
    brand_arr.append(kit.brand)
  brands = set(brand_arr)

  rdm = generate_random_file_name(8)
  date = order.date_processed.strftime("%Y_%m_%d")
  excel_file = f"{order.user}_order_{date}_{rdm}.csv"
  full_path = folder + excel_file

  with default_storage.open(full_path, 'w') as file:

    for brand in brands:
      writer = csv.writer(file)
      field = ['Catalog number', 'Quantity', brand.name.upper()]

      writer.writerow(field)
      for input in inputs:   
        if input['brand'] == brand.name:
          writer.writerow([input['catalog_number'], input['amount']])

  order.orders_file = full_path
  order.save()


def kit_to_inventory(kit, user, lot_number):

  for reagent in kit.storereagent_set.all():
    Reagent.objects.create(
      user = user,
      name = reagent.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      usage = reagent.usage,
      pcr_reagent = reagent.pcr_reagent,
      volume = reagent.volume,
      unit_volume = reagent.unit_volume,
      stock_concentration = reagent.stock_concentration,
      unit_concentration = reagent.unit_concentration,
      forward_sequence = reagent.forward_sequence,
      reverse_sequence = reagent.reverse_sequence,
    )

  for tube in kit.storetube_set.all():
    Tube.objects.create(
      user = user,
      name = tube.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      amount = tube.amount,
    )

  for gel in kit.storegel_set.all():
    Gel.objects.create(
      user = user,
      name = gel.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      size = gel.size,
      amount = gel.amount,
    )

  for plate in kit.storeplate_set.all():
    Plate.objects.create(
      user = user,
      name = plate.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      size = plate.size,
      type = plate.type,
      amount = plate.amount,
    )
  
  for dye in kit.storedye_set.all():
    Dye.objects.create(
      user = user,
      name = dye.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      amount = dye.amount,
    )

  for ladder in kit.storeladder_set.all():
    Ladder.objects.create(
      user = user,
      name = ladder.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      amount = ladder.amount,
    )