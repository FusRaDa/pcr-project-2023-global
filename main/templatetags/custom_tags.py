from django import template
from decimal import Decimal

register = template.Library()

def dec_mult(value, arg):
  product = Decimal(value*arg)
  return product

register.filter("dec_mult", dec_mult)


