from __future__ import unicode_literals
from django.db import models
from itertools import chain
from operator import attrgetter
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from chama.models import Member, Account
from django.utils import timezone

YEAR = 'year'
MONTH = 'month'
WEEK = 'week'
DAY = 'day'
INTERVAL_CHOICES = ((YEAR, 'per anum'), (MONTH, 'per month'), (WEEK, 'per week'), (DAY, 'per day'),)
FIXED = 'fixed'
CONTRACT = 'contract'
CURRENT = 'current'
TARGET = 'target'
TYPE_CHOICES = ((FIXED, 'fixed'), (CONTRACT, 'contract'), (CURRENT, 'current'), (TARGET, 'target'),)

class Type(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=TYPE_CHOICES, default=FIXED)
    interval = models.CharField(max_length=100, choices=INTERVAL_CHOICES, default=MONTH)
    min_amount = models.IntegerField()
    max_amount = models.IntegerField()
    compulsory = models.BooleanField(default=True)
    interest_rate = models.IntegerField()

    def __str__(self):
        return self.name

class Savings(models.Model):
    class Meta:
        verbose_name_plural = 'savings'

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    savings_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return ''.join([self.member.user.first_name, self.member.user.last_name])
    
    def member_name(self):
        return ''.join([self.member.user.first_name, self.member.user.last_name])

    @classmethod
    def get_members_savings(cls, member, current_savings_type=None):
        if current_savings_type is None:
            savings = cls.objects.filter(member=member)

        else:
            savings = cls.objects.filter(savings_type=current_savings_type, member=member)

        return savings

    @classmethod
    def get_members_savings_total(cls, member):
        savings = cls.objects.filter(member=member).aggregate(Sum('amount'))
        return savings['amount__sum']

    @classmethod
    def get_savings(cls, members=None, current_savings_type=None):
        savings = []
        if current_savings_type is None:
            if members is None:
                savings = cls.objects.all()
            elif isinstance(members, Member):
                savings = cls.objects.filter(member=members)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                savings = cls.objects.filter(member__in=account_members)
            elif isinstance(members, list):
                savings = cls.objects.filter(member__in=members)

        elif isinstance(current_savings_type, Type):
            if members is None:
                savings = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                savings = cls.objects.filter(member=members, savings_type=current_savings_type)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                savings = cls.objects.filter(member__in=account_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                savings = cls.objects.filter(member__in=members, savings_type=current_savings_type)

        return savings

    @classmethod
    def get_savings_transactions(self, member):
        return sorted(chain(SavingsDeposit.get_savings_deposit(member), SavingsWithdrawal.get_savings_withdrawal(member)), key=attrgetter('date'))


class SavingsWithdrawal(models.Model):
    amount = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    savings_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    date = models.DateField()

    @classmethod
    def withdraw_savings(cls, member, amount, savings_type):
        try:
            savings = Savings.objects.get(member=member, savings_type=savings_type)
        except ObjectDoesNotExist:
            return ValidationError({"savings_type": "You do not have any savings of type" + savings_type.__str__()})
        if savings < amount:
            return ValidationError({"amount": "You do not have enough savings in your savings type of" + savings_type.__str__()})

        savings_withdrawal = cls(amount=amount, savings_type=savings_type, member=member, date=timezone.now())
        savings.amount -= amount
        savings_withdrawal.save()
        savings.save()
        return savings_withdrawal

    @classmethod
    def get_withdrawals(cls, members=None, current_savings_type=None):
        if current_savings_type is None:
            if members is None:
                withdrawals = cls.objects.all()
            elif isinstance(members, Member):
                withdrawals = cls.objects.filter(member=members)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                withdrawals = cls.objects.filter(member__in=account_members)
            elif isinstance(members, list):
                withdrawals = cls.objects.filter(member__in=members)
        elif isinstance(current_savings_type, Type):
            if members is None:
                withdrawals = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                withdrawals = cls.objects.filter(member=members, savings_type=current_savings_type)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                withdrawals = cls.objects.filter(member__in=account_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                withdrawals = cls.objects.filter(member__in=members, savings_type=current_savings_type)
        else:
            withdrawals = []
        return withdrawals

class SavingsDeposit(models.Model):
    amount = models.IntegerField()
    date = models.DateField(blank=True, auto_now_add=True)
    savings_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Savings Purchase'

    @classmethod
    def deposit_savings(cls, member, amount, savings_type, date=timezone.now()):
        try:
            savings = Savings.objects.get(member=member, savings_type=savings_type)
            savings.amount += amount
        except ObjectDoesNotExist:
            savings = Savings.objects.get(member=member, amount=amount, savings_type=savings_type, date=date)
        finally:
            deposit = cls(member=member, amount=amount, savings_type=savings_type, date=date)
            deposit.save()
            savings.save()
            return deposit

    @classmethod
    def get_savings_deposit(cls, members=None, current_savings_type=None):
        if current_savings_type is None:
            if members is None:
                deposits =  cls.objects.all()
            elif isinstance(members, Member):
                deposits = cls.objects.filter(member=members)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                deposits = cls.objects.filter(member__in=account_members)
            elif isinstance(members, list):
                deposits = cls.objects.filter(member__in=members)
        elif isinstance(current_savings_type, Type):
            if members is None:
                deposits = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                deposits = cls.objects.filter(memebr=members, savings_type=current_savings_type)
            elif isinstance(members, Account):
                account_members = Member.objects.filter(account__pk=members.pk)
                deposits = cls.objects.filter(member__in=account_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                deposits = cls.objects.filter(member__in=members, savings_type=current_savings_type)
        else:
            deposits = []
        return deposits




















