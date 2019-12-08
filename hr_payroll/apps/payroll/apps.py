from django.apps import AppConfig


class PayrollConfig(AppConfig):
    name = 'hr_payroll.apps.payroll'
    verbose_name = 'Nómina'

    def ready(self):
        import hr_payroll.apps.payroll.signals
