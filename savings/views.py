from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from savings.forms import SavingsForm, SavingsWithdrawalForm, SavingsDepositForm
from django.contrib import messages


def savings_view(request):
	
	if request.method == 'POST':
		savings_form = SavingsForm(request.POST)

		if savings_form.is_valid():
			savings = savings_form.save(commit=True)
			amount = savings_form.cleaned_data['amount']
			member = savings_form.cleaned_data['member']
			savings.save()
			messages.success(request, 'Savings of ' + str(amount) + ' was submitted successfully for member ' + str(member) + ' , please confirm balance!')
			return redirect(reverse('savings:savings'))

	else:
		savings_form = SavingsForm()

	return render(request, 'savings/savings.html', {'savings_form': savings_form})


def withdraw_view(request):
	if request.method == 'POST':
		withdraw_form = SavingsWithdrawalForm(request.POST)

		if withdraw_form.is_valid():
			withdraw = withdraw_form.save(commit=True)
			Amount = withdraw_form.cleaned_data['amount']
			member = withdraw_form.cleaned_data['member']
			withdraw.save()
			messages.success(request, str(Amount) + ' has been withdrawn from ' + str(member) + ' savings account, please confirm your balance!')
			return redirect(reverse('savings:withdraw'))

	else:
		withdraw_form = SavingsWithdrawalForm()

	return render(request, 'savings/withdraw.html', {'withdraw_form': withdraw_form})


def deposit_view(request):
	if request.method == 'POST':
		deposit_form = SavingsDepositForm(request.POST)

		if deposit_form.is_valid():
			deposit = deposit_form.save(commit=True)
			amount = deposit_form.cleaned_data['amount']
			member = deposit_form.cleaned_data['member']
			deposit.save()
			messages.success(request, str(amount) + ' has been deposited into ' + str(member) + ' savings account, please confirm balance!')
			return redirect(reverse('savings:deposit'))

	else:
		deposit_form = SavingsDepositForm()

	return render(request, 'savings/deposit.html', {'deposit_form': deposit_form})