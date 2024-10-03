from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from sbank.models import Account, Transaction, MyUser
import random


# ACCOUNT NUMBER GENERATOR
def account_num():
    """Function to generate account number"""
    bank_code = '1218'
    min_val = 0
    max_val = 999999
    user_num = random.randint(min_val, max_val)
    result = int(bank_code + str(user_num))
    return result


# HOME PAGE
def index(request):
    """Index page"""
    return render(request, 'sbank/index.html')


# DASHBOARD VIEW
@login_required(login_url='/login')
def dashboard(request):
    """Dashboard view"""
    user = request.user
    account = Account.objects.filter(username=user).first()
    if account:
        data = {
            'account_no': account.account_no,
            'balance': account.balance
        }
    else:
        data = {
            'account_no': 'N/A',
            'balance': 'N/A'
        }
    return render(request, 'sbank/dashboard.html', data)
    

# CREATE ACCOUNT
@login_required(login_url='/login')
def create_account(request, balance = 100):
    """Function to create an account"""
    if request.method == 'POST':
        user_name = request.user
        user_acc = account_num()
        if not Account.objects.filter(account_no=user_acc).exists():
            account = Account.objects.create(
                balance=balance,
                account_no=user_acc,
                username=user_name)
            account.save()
            redirect('dashboard')
    return render(request, 'sbank/404-page.html')


@login_required(login_url='/login')
def deposit(request):
    """Function to make a deposit"""
    if request.method == 'POST':
        try:
            deposit_amount = float(request.POST.get('balance'))
        except (TypeError, ValueError):
            return render(request, 'sbank/404-page.html')

        user = request.user
        account = Account.objects.filter(username=user).first()
        if deposit_amount > 0 and account:
            account.balance += deposit_amount
            account.save()
            return redirect('dashboard')
    return render(request, 'sbank/404-page.html')

