from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from users.models import User
from ..models.affiliates import Brand


class Tag(models.Model):
  name = models.CharField(blank=False, max_length=50, unique=True)

  def __str__(self):
    return self.name


class Kit(models.Model):
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

  image = models.ImageField(null=True, blank=True, upload_to='kits')

  name = models.CharField(blank=False, max_length=250)
  description = models.TextField(blank=False, default="Kit Description")
  catalog_number = models.CharField(blank=False, max_length=25)
  price = models.DecimalField(blank=False, decimal_places=2, max_digits=7) #USD

  affiliate_link = models.URLField(max_length=200, blank=True, null=True)

  tags = models.ManyToManyField(Tag)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['brand', 'catalog_number'], 
        name='kit_unique',
        violation_error_message = "A kit with the same brand and catalog number already exists.",
      )
    ]

  @property
  def avg_rating(self):
    reviews = self.review_set.all()
    if len(reviews) > 0:
      review_num = 0
      sum = 0
      for review in reviews:
        sum += review.rating
        review_num += 1
      avg = int(sum / review_num)
      return avg
    else:
      return None
    
  @property
  def review_num(self):
    return self.review_set.count()
  
  @property
  def abs_url(self):
    try:
      url = self.image.url
      abs = url.replace("/main", "")
      return abs
    except ValueError:
      return '/static/kits/default-kit.png'
    
  def __str__(self):
    return f"{self.name}-{self.catalog_number}"


class StoreLadder(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=100, default="LADDER")
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)  # microliters

  def __str__(self):
    return self.name


class StoreDye(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=100, default="DYE")
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)  # microliters

  def __str__(self):
    return self.name


class StorePlate(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
  
  class Sizes(models.IntegerChoices):
    EIGHT = 8, _('8')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')
    NINETY_SIX = 96, _('96')
    THREE_HUNDRED_EIGHTY_FOUR = 384, _('384')

  class Types(models.TextChoices):
    PCR = 'PCR', _('PCR')
    qPCR = 'qPCR', _('qPCR')

  name = models.CharField(blank=False, max_length=100, default="PLATE")
  size = models.IntegerField(choices=Sizes.choices, default=Sizes.NINETY_SIX, blank=False)
  type = models.CharField(choices=Types.choices, blank=False, default=Types.PCR, max_length=25)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  def __str__(self):
    return self.name
  

class StoreGel(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  class Sizes(models.IntegerChoices):
    TWELVE = 12, _('12')
    TWENTY_FOUR = 24, _('24')
    FOURTY_EIGHT = 48, _('48')

  name = models.CharField(blank=False, max_length=100, default="GEL")
  size = models.IntegerField(choices=Sizes.choices, default=Sizes.TWENTY_FOUR, blank=False)
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  def __str__(self):
    return self.name


class StoreTube(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  name = models.CharField(blank=False, max_length=100, default="TUBE")
  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  def __str__(self):
    return self.name
  

# class StoreControl(models.Model):
#   kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

#   name = models.CharField(blank=False, max_length=100)
#   amount = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12) # in microliters

#   def __str__(self):
#     return self.name
  

class StoreReagent(models.Model):
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  class Usages(models.TextChoices):
    EXTRACTION = 'EXTRACTION', _('EXTRACTION')
    PCR = 'PCR', _('PCR')

  class VolumeUnits(models.TextChoices):
    LITER = 'L', _('L')
    MILLILITER = 'mL', _('mL')
    MICROLITER = '\u00B5L', _('\u00B5L')

  class ConcentrationUnits(models.TextChoices):
    MOLES = 'M', _('M')
    MILLIMOLES = 'mM', _('mM')
    MICROMOLES = '\u00B5M', _('\u00B5M')
    NANOMOLES = 'nM', _('nM')
    UNITS = 'U/\u00B5L', _('U/\u00B5L')
    X = 'X', _('X')

  class PCRReagent(models.TextChoices):
    GENERAL = 'GENERAL', _('General')
    PRIMER = 'PRIMER', _('Primer')
    POLYMERASE = 'POLYMERASE', _('Polymerase') #used as units/micro-liter
    WATER = 'WATER', _('Water')

  name = models.CharField(blank=False, max_length=100, default="REAGENT")
  usage = models.CharField(choices=Usages.choices, blank=False, default=Usages.PCR, max_length=25)
  pcr_reagent = models.CharField(choices=PCRReagent.choices, blank=True, null=True, default=None, max_length=25) # determine calculations for type of pcr reagent
 
  volume = models.DecimalField(decimal_places=2, blank=False, validators=[MinValueValidator(0)], max_digits=12, default=1)
  unit_volume = models.CharField(choices=VolumeUnits.choices, blank=False, default=VolumeUnits.MICROLITER, max_length=25)

  stock_concentration = models.DecimalField(decimal_places=2, blank=True, null=True, default=None, validators=[MinValueValidator(0)], max_digits=12)
  unit_concentration = models.CharField(choices=ConcentrationUnits.choices, blank=True, null=True, default=None, max_length=25)

  forward_sequence = models.CharField(blank=True, null=True, max_length=100) # 3 to 5
  reverse_sequence = models.CharField(blank=True, null=True, max_length=100) # 5 to 3
  
  def __str__(self):
    return self.name
  

class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  text = models.TextField(blank=False)

  rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5) # https://www.w3schools.com/howto/howto_css_star_rating.asp
  is_reported = models.BooleanField(default=False)

  date_updated = models.DateField(default=now)

  def __str__(self):
    return f"{self.kit.name} by {self.user}"