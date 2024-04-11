from django import template

register = template.Library()


@register.filter
def is_vendor(user):
    return user.groups.filter(name='Vendor').exists()