from django.apps import AppConfig


class PollsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollsapp'

    def ready(self):
        from . import signals