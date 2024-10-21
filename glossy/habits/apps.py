from django.apps import AppConfig


class HabitsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habits"

    def ready(self):
        import api.v1.services.cache_signals
        import habits.signals

