from __future__ import unicode_literals
from django.contrib import admin
from savings.models import Savings, Type, SavingsWithdrawal, SavingsDeposit

class SavingsAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'date', 'amount')
    readonly_fields = ('member', 'savings_type', 'date', 'amount')

class SavingsWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'date', 'amount')
    def save_model(self, request, obj, form, change):
        SavingsWithdrawal.withdraw_savings(obj.member, obj.savings_type, obj.amount)

class SavingsDepositAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'date', 'amount')
    def save_model(self, request, obj, form, change):
        SavingsDeposit.deposit_savings(obj.member, obj.savings_type, obj.amount)

class SavingsAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'date', 'amount')
    list_filter = ('savings_type', 'date', 'amount')
    search_fields = []

class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'interval', 'min_amount', 'max_amount', 'compulsory', 'interest_rate')
    list_filter = ('name',)
    search_fields = ['name', 'category']

admin.site.register(Savings, SavingsAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(SavingsWithdrawal, SavingsWithdrawalAdmin)
admin.site.register(SavingsDeposit, SavingsDepositAdmin)
















