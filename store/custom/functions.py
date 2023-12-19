import csv
from zipfile import ZipFile
import os

def generate_order_files(order, zipped_data):
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
      for order_kits, kits in zipped_data:
        if order_kits.brand == brand:
          writer.writerow([order_kits.catalog_number, kits.amount_ordered])

    files.append(file)

  for file in files:
    print(file.name)

  zip_file_name = path + f"order_list_{order.date_file}.zip"
  with ZipFile(zip_file_name, 'w') as zipf:

    for file in files:
      arcname = file.name.rsplit('/', 1)[-1]
      zipf.write(file.name, arcname=arcname)
      os.remove(file.name)

