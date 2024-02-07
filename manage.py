#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import call_command


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_app.settings")
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
    
    from weather_app.backend.location.models import UserLocationModel

    UserLocationModel.objects.all().delete()

def test():
    test_failures = call_command('test')
    if test_failures:
        sys.exit(test_failures)

if __name__ == "__main__":
    main()
    test()