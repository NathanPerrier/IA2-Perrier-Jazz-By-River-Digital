from django import template
from datetime import datetime, timedelta
import pytz
from django.utils import timezone

register = template.Library()

@register.filter
def div(amount, value):
    return "{:.2f}".format(amount/value)

@register.filter
def add_date(date):
    created = date
    # Convert the Unix timestamp to a datetime object
    created_date = datetime.fromtimestamp(created)
    # Add 2 minutes
    created_date += timedelta(minutes=2)
    
    return created_date

@register.filter
def add_day(date):
    created = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    # Add 2 days
    created_date = created + timedelta(days=1)
    
    return created_date
