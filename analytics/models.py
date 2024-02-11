from django.db import models
from django.utils.timezone import now

from users.models import User

# Create your models here.

class LoginAction(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField(default=now().date(), editable=False)

  def __str__(self):
    return f'{self.user}-{self.date}'

