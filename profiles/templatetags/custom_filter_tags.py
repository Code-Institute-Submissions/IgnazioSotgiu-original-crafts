from django import template

register = template.Library()


@register.filter
def update_variable(value):
    return True
