from django import template

register = template.Library()


@register.filter
def is_vendor(user):
    return user.groups.filter(name='Vendor').exists()

@register.filter
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@register.filter
def is_student(user):
    return user.groups.filter(name='Student').exists()

@register.filter
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

@register.filter
def is_parent(user):
    return user.groups.filter(name='Parent').exists()

@register.filter
def is_user(user):
    return user.groups.filter(name='User').exists()

@register.filter
def is_staff(user):
    return user.groups.filter(name='Staff').exists()

@register.filter
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

@register.filter
def is_volunteer(user):
    return user.groups.filter(name='Volunteer').exists()

@register.filter
def is_guest(user):
    return user.groups.filter(name='Guest').exists()

@register.filter
def is_year(user, i):
    return user.groups.filter(name='Year '+str(i)).exists()

@register.filter
def in_target_groups(user, event):
    return event.target_groups.filter(id__in=user.groups.all()).exists()


@register.filter
def rangefilter(value):
    return range(1, value + 1)


@register.filter
def split(value, key):
    return value.split(key)

@register.filter
def multiply(value1, value2):
    return value1*value2


@register.filter
def total_vendor_price(invoice_lines, vendor_items):
    return sum(item.amount for item in invoice_lines if item.description in vendor_items)