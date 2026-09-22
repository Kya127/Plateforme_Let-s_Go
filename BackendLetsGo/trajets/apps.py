from django.apps import AppConfig


class TrajetsConfig(AppConfig):
    name = 'trajets'


    def ready(self):
        import trajets.signals