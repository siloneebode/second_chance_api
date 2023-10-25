from django.apps import AppConfig


class FollowerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Domain.follower'

    def ready(self):
        import Domain.follower.signals
