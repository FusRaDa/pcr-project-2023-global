from django import template
from decimal import Decimal

register = template.Library()

def dec_mult(value, arg):
  product = Decimal(value*arg)
  return product

def dec_mult_string(value, arg):
  product = Decimal(value*arg)
  return "{:.2f}".format(product)

def remaining_amounts(value, arg):
  return round(float(arg) - float(value), 2)

def round_str(value, arg):
  dec = round(value, arg)
  return dec

register.filter("dec_mult", dec_mult)
register.filter("remaining_amounts", remaining_amounts)
register.filter("dec_mult_string", dec_mult_string)
register.filter("round_str", round_str)


