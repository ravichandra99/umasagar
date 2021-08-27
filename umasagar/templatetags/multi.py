from django import template
from umasagar.models import SaleBill

register = template.Library()


@register.simple_tag
def multi(a,b):
	return round(a * b,2)

