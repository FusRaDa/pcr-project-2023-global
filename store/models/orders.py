from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from users.models import User
from ..models.items import Kit


# one order can only have on kit/product 
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  kits = models.ManyToManyField(Kit, through='KitOrder')

  date_added = models.DateTimeField(default=now, editable=False)
  has_ordered = models.BooleanField(blank=False, default=False)

  @property
  def total_cost(self):
    cost = 0
    amounts = self.kitorder_set.all()
    for amount in amounts:
      cost += amount.kit.price * amount.amount_ordered
    return cost

  def __str__(self):
    return f"Order - {self.date_added}"
  

class KitOrder(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  amount_ordered = models.IntegerField(validators=[MinValueValidator(1)], default=1)

  def __str__(self):
    return f"Through - {self.kit.name}"