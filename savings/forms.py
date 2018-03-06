from django import forms
from savings.models import Savings, SavingsWithdrawal, SavingsDeposit, Type


class SavingsForm(forms.ModelForm):

    class Meta:
        model = Savings
        fields = (
            'member',
            'savings_type',
            'amount'
        )


class SavingsWithdrawalForm(forms.ModelForm):
	class Meta:
		model = SavingsWithdrawal
		fields = (
			'amount',
			'member',
			'savings_type',
			'date'
		)


class SavingsDepositForm(forms.ModelForm):
	class Meta:
		model = SavingsDeposit
		fields = (
			'amount',
			'savings_type',
			'member'
		)