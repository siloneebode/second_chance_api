from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Domain.account'
    label = 'Domain_account'

    def ready(self):
        import second_chance_api.celery