from django.contrib import admin
from hr_payroll.apps.payroll import models
import requests


@admin.register(models.Payroll)
class PayrollAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = (
        'id',
        'payroll_type',
        'date',
        'total_incomes',
        'total_deductions',
        'grand_total',
    )
    list_filter = (
        'payroll_type',
        'date',
    )


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def upload_accounting_entries(self, request, queryset):
        for transaction in queryset:
            data = {
                "accountingEntryCredit": {
                    "description": f"Movimiento de Nómina: {transaction}",
                    "auxiliaryAccountId": 2,
                    "account": transaction.transaction_type.name,
                    "movementType": 0,
                    "period": f"{transaction.payroll.date}",
                    "amount": float(transaction.amount),
                    "currencyTypeId": 1
                }, "accountingEntryDebit": {
                    "description": f"Movimiento de Nómina: {transaction}",
                    "auxiliaryAccountId": 2,
                    "account": transaction.transaction_type.name,
                    "movementType": 1,
                    "period": f"{transaction.payroll.date}",
                    "amount": float(transaction.amount),
                    "currencyTypeId": 1
                }
            } if transaction.transaction_type.transaction_type == 'DE' else {
                "accountingEntryCredit": {
                    "description": f"Movimiento de Nómina: {transaction}",
                    "auxiliaryAccountId": 2,
                    "account": transaction.transaction_type.name,
                    "movementType": 0,
                    "period": f"{transaction.payroll.date}",
                    "amount": float(transaction.amount),
                    "currencyTypeId": 1
                }, "accountingEntryDebit": {
                    "description": f"Movimiento de Nómina: {transaction}",
                    "auxiliaryAccountId": 2,
                    "account": transaction.transaction_type.name,
                    "movementType": 1,
                    "period": f"{transaction.payroll.date}",
                    "amount": float(transaction.amount),
                    "currencyTypeId": 1
                }
            }

            print(data)
            response = requests.post(
                url="https://apecaccountingapi.azurewebsites.net/api/account-entry",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            print(response.json())

        self.message_user(request, f'Operación realizada con éxito.')

    upload_accounting_entries.short_description = f"Enviar {models.Transaction._meta.verbose_name_plural} seleccionado/s a contabilidad"

    date_hierarchy = 'payroll__date'
    list_display = (
        'id',
        'payroll',
        'employee',
        'transaction_type',
        'amount',
    )
    list_filter = (
        'payroll',
        'employee',
        'transaction_type',
    )
    search_fields = (
        'payroll_id__date',
        'employee_id__first_name',
        'employee_id__last_name',
        'transaction_type_id__name',
        'amount',
    )
    actions = [upload_accounting_entries]
