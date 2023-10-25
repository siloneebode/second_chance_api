from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Domain.auth'
    label = 'Domain_auth'

    def ready(self):
        import Domain.auth.Utils.signals
