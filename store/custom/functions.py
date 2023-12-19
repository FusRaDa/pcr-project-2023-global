import csv
from zipfile import ZipFile

def generate_order_files(order, zipped_data):

  brand_arr = []
  for kit in order.kits.all():
    brand_arr.append(kit.brand)

  brands = set(brand_arr)

  for brand in brands:

    path = 'static/files/'
    with open(path + f"{brand}_order_list_{order.pk}.csv", 'w', newline='') as file:
      writer = csv.writer(file)
      field = ['Catalog number', 'Quantity']

      writer.writerow(field)
      for order_kits, kits in zipped_data:
        if order_kits.brand == brand:
          writer.writerow([order_kits.catalog_number, kits.amount_ordered])

  # with ZipFile(path + 'students.zip', 'w') as zipf:
  #   zipf.write(path + 'students.csv', arcname='students.csv')

