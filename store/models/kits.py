from django.db import models

class Brand(models.Model):
  name = models.CharField(blank=False, max_length=25)