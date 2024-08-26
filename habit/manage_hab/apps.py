from django.apps import AppConfig


class ManageHabConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manage_hab"

    def ready(self):
        import habit_api.services.cache_signals
        import manage_hab.signals

