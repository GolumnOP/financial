from django.contrib import admin

from accounting.models import BalanceSheetItem, BalanceGroup, Account


@admin.register(BalanceSheetItem)
class BalanceSheetItemAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(BalanceGroup)
class BalanceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance_sheet')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'type', 'balance')

# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('')
