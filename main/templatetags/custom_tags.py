from django import template
from decimal import Decimal

register = template.Library()

def dec_mult(value, arg):
  product = Decimal(value*arg)
  return "{:.2f}".format(product)

def remaining_amounts(value, arg):
  return arg - value

register.filter("dec_mult", dec_mult)
register.filter("remaining_amounts", remaining_amounts)


