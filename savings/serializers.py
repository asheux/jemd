from django.contrib,auth.models import User
from rest_framework import serializers, viewsets
from chama.serializers import MemberSerializer, MemberUserSerializer
from chama.models import Member, Account
from savings.models import Savings, Type, SavingsDeposit, SavingsWithdrawal

class SavingsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fileds = ('name', 'category', 'interval', 'min_amount', 'max_amount', 'compulsory', 'interest_rate')

class SavingsSerializer(serializers.ModelSerializer):
    member = MemberSerializer()
    savings_type = SavingsTypeSerializer()
    class Meta:
        model = Savings
        fields = ('id', 'member', 'amount', 'date', 'savings_type')

class CreateSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = ('id', 'member', 'amount', 'date', 'savings_type')

class SavingsWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsWithdrawal
        fields  ('id', 'member', 'amount', 'date', 'savings_type')


class SavingsMinimalSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    savings_type = SavingsTypeSerializer()

    class Meta:
        model = savings
        fields = ('id', 'member', 'amount', 'date', 'savings_type')

class SavingsDepositMinimalSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()

    class Meta:
        model = SavingsDeposit
        fields = ('id', 'member', 'amount', 'date', 'savings_type')


class SavingsDepositPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsDeposit
        fields = ('amount', 'savings_type')

class SavingsWithdrawalMinimalSerializer(serializers.ModelSerializer):
    memmber = MemberUserSerializer()

    class Meta:
        model = SavingsWithdrawal
        fields = ('id', 'member', 'amount', 'date', 'savings_type')

class SavingsWithdrawalPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsWithdrawal
        fields = ('amount', 'savings_type')

class SavingsWithdrawalTransactionSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = SavingsWithdrawal

    def get_transaction_type(self, obj):
        return obj.__class__.__name__

class SavingsDepositTransactionSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model SavingsDeposit

    def get_transaction_type(self, obj):
        return obj.__class__.__name__
















