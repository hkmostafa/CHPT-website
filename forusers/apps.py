from django.apps import AppConfig


class ForusersConfig(AppConfig):
    name = 'forusers'

    def ready(self):
        import forusers.signals