from django import template

register = template.Library()


@register.filter(name='update_var')
def update_var(val):
    return val
