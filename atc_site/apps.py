from django.apps import AppConfig

class ATC_SiteConfig(AppConfig):
    name = 'atc_site'

    def ready(self):
        import atc_site.signals  