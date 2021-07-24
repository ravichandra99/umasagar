from django import template

register = template.Library()


@register.simple_tag
def multi(a,b):
	return round(a * b,2)