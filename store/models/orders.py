from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from users.models import User

from ..models.items import Kit


# one order can only have on kit/product 
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  kit = models.ForeignKey(Kit, on_delete=models.SET_NULL)

  date_added = models.DateTimeField(default=now, editable=False)
  has_ordered = models.BooleanField(blank=False, default=False)

  def __str__(self):
    return f"{self.kit}-{self.user.username}"




  