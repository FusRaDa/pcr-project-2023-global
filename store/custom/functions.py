import csv
from zipfile import ZipFile
import os

from django.core.files import File

from pcr.models.inventory import Tube, Plate, Reagent

def generate_order_files(order, inputs):
  path = 'static/orders/'

  brand_arr = []
  for kit in order.kits.all():
    brand_arr.append(kit.brand)

  brands = set(brand_arr)

  files = []
  for brand in brands:

    with open(path + f"{brand}_order_list_{order.pk}.csv", 'w', newline='') as file:
      writer = csv.writer(file)
      field = ['Catalog number', 'Quantity']

      writer.writerow(field)
      for input in inputs:   
        if input['brand'] == brand.name:
          writer.writerow([input['catalog_number'], input['amount']])
    
    files.append(file.name)
  
  file_path = path + f"order_{order.pk}_list_{order.date_file}.zip"
  with ZipFile(file_path, 'w') as zipf:

    for file in files:
      arcname = file.rsplit('/', 1)[-1]
      zipf.write(file, arcname=arcname)
      os.remove(file)

  local_file = open(file_path, 'rb')
  order.orders_file.save(f"order_{order.pk}_list_{order.date_file}.zip", local_file)
  local_file.close()



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

  for plate in kit.storeplate_set.all():
    Plate.objects.create(
      user = user,
      name = plate.name,
      brand = kit.brand,
      lot_number = lot_number,
      catalog_number = kit.catalog_number,
      size = plate.size,
      amount = plate.amount,
    )

