from django import template
from datetime import datetime, timedelta
import pytz
from atc_site.backend.location.main import GetLocation

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