import csv
from zipfile import ZipFile
import os

def generate_order_files(order, inputs):
  path = 'static/files/'

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

  with ZipFile(path + f"order_{order.pk}_list_{order.date_file}.zip", 'w') as zipf:

    for file in files:
      arcname = file.rsplit('/', 1)[-1]
      zipf.write(file, arcname=arcname)
      os.remove(file)

