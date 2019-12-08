from django.db import models
from hr_payroll.apps.employees.models import Employee


class PayrollType(models.Model):
    name = models.CharField(verbose_name='nombre',
                            max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'tipo de nómina'
        verbose_name_plural = 'tipos de nómina'

    def __str__(self):
        return self.name


class Payroll(models.Model):
    payroll_type = models.ForeignKey(
        to=PayrollType, on_delete=models.CASCADE, verbose_name='tipo de nómina')
    date = models.DateField(verbose_name='fecha')

    class Meta:
        verbose_name = 'nómina'
        verbose_name_plural = 'nóminas'
        constraints = [models.UniqueConstraint(
            fields=['payroll_type', 'date'], name='payroll__unique__payroll_type__date')]

    def __str__(self):
        return str(self.date)

    def total_incomes(self):
        return self.transaction_set.all().filter(transaction_type__transaction_type='IN').aggregate(models.Sum('amount')).get('amount__sum')
    total_incomes.short_description = 'total ingresos'

    def total_deductions(self):
        return self.transaction_set.all().filter(transaction_type__transaction_type='DE').aggregate(models.Sum('amount')).get('amount__sum')
    total_deductions.short_description = 'total deducciones'

    def grand_total(self):
        return self.total_incomes() - self.total_deductions()
    grand_total.short_description = 'total'


class TransactionType(models.Model):
    name = models.CharField(verbose_name='nombre',
                            max_length=30, blank=False, null=False)
    transaction_type = models.CharField(verbose_name='tipo de transacción', max_length=2, choices=[
                                        ('IN', 'Ingreso'), ('DE', 'Deducción')], blank=False, null=False)
    depends_salary = models.BooleanField(
        verbose_name='depende de salario', default=False)
    amount = models.DecimalField(
        verbose_name='monto', max_digits=14, decimal_places=4, null=False, blank=False)
    active = models.BooleanField(verbose_name='activo', default=True)

    class Meta:
        verbose_name = 'tipo de transacción'
        verbose_name_plural = 'tipos de transacción'

    def __str__(self):
        choices = {'IN': 'Ingreso', 'DE': 'Deducción'}
        return f'{self.name} ({choices[self.transaction_type]}{", depende de salario" if not self.depends_salary else ""})'


class Transaction(models.Model):
    payroll = models.ForeignKey(
        to=Payroll, on_delete=models.CASCADE, verbose_name='nómina')
    employee = models.ForeignKey(
        to=Employee, on_delete=models.CASCADE, verbose_name='empleado')
    transaction_type = models.ForeignKey(to=TransactionType, on_delete=models.CASCADE,
                                         verbose_name='tipo de transacción')
    amount = models.DecimalField(
        verbose_name='monto', max_digits=14, decimal_places=4, null=False, blank=False)

    class Meta:
        verbose_name = 'transacción'
        verbose_name_plural = 'transacciones'

    def __str__(self):
        return f'[{self.id}] {self.employee} ({self.transaction_type.name}): {self.amount}'
