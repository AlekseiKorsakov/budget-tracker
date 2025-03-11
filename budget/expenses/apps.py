from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
    verbose_name = 'Budget tracker'

    def ready(self):
        import expenses.signals
