from django.apps import AppConfig


class BudgetConfig(AppConfig):
    name = 'budget'

    def ready(self):
        import budget.signals