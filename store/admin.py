from django.contrib import admin

from models.affiliates import Brand, Contact
from models.items import Kit, StorePlate, StoreTube, StoreReagent
from models.orders import Order
# Register your models here.

admin.site.register(Brand, Contact)
admin.site.register(Kit, StorePlate, StoreTube, StoreReagent)
admin.site.register(Order)
