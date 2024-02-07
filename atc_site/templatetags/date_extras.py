from django import template
from datetime import timedelta
import datetime
import pytz
from atc_site.backend.location.main import GetLocation

register = template.Library()

@register.filter
def add_days(date, days):
    return date + timedelta(days=days)

@register.filter
def add_day():
    current_date = datetime.datetime.now(pytz.timezone(GetLocation().get_location().timezone))
    return current_date + timedelta(days=1)