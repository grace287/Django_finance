from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account
from apps.transactions.models import Transaction
from apps.transactions.forms import TransactionForm
from .forms import AccountCreateForm, AccountUpdateForm
from django.contrib import messages
import random


@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, '계좌 정보가 수정되었습니다.')
            return redirect('accounts:account_detail', pk=account.pk)
    else:
        form = AccountUpdateForm(instance=account)
    
    return render(request, 'accounts/account_update.html', {
        'form': form,
        'account': account
    })

def account_list(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account})

def account_create(request):
    if request.method == 'POST':
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            try:
                # 최대 계좌 수 확인
                if Account.objects.filter(user=request.user, is_active=True).count() >= 3:
                    messages.error(request, '최대 3개의 계좌만 개설할 수 있습니다.')
                    return redirect('accounts:account_list')

                # 계좌번호 생성
                while True:
                    bank_code = form.cleaned_data['bank_code']
                    account_number = f"{bank_code}{''.join([str(random.randint(0, 9)) for _ in range(12)])}"
                    if not Account.objects.filter(account_number=account_number).exists():
                        break

                # 계좌 생성
                account = form.save(commit=False)
                account.user = request.user
                account.account_number = account_number
                account.balance = form.cleaned_data['initial_balance']
                account.save()

                # 초기 입금 내역 생성
                if account.balance > 0:
                    TransactionHistory.objects.create(
                        account=account,
                        transaction_type='deposit',
                        amount=account.balance,
                        description='계좌 개설 초기 입금'
                    )

                messages.success(request, '계좌가 성공적으로 생성되었습니다.')
                return redirect('accounts:account_detail', pk=account.pk)

            except Exception as e:
                messages.error(request, f'계좌 생성 중 오류가 발생했습니다: {str(e)}')
                return redirect('accounts:account_list')
    else:
        form = AccountCreateForm()

    return render(request, 'accounts/account_create.html', {'form': form})

def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        if account.balance > 0:
            messages.error(request, '잔액이 있는 계좌는 삭제할 수 없습니다.')
            return redirect('accounts:account_detail', pk=account.pk)
        
        # 계좌 비활성화 (실제 삭제 대신)
        account.is_active = False
        account.save()
        
        messages.success(request, '계좌가 삭제되었습니다.')
        return redirect('accounts:account_list')
        
    return render(request, 'accounts/account_delete.html', {'account': account})

def account_transaction_list(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')
    return render(request, 'accounts/transaction_list.html', {
        'account': account,
        'transactions': transactions
    })

def transaction_home(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/transaction_home.html', {'accounts': accounts})


# def transaction_create(request, pk):
#     account = get_object_or_404(Account, pk=pk, user=request.user)
#     transaction_type = request.GET.get('type', 'deposit')
    
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.account = account
#             transaction.transaction_type = transaction_type
#             transaction.save()
#             return redirect('accounts:account_transaction_list', pk=pk)
#     else:
#         form = TransactionForm()
    
#     return render(request, 'accounts/transaction_form.html', {
#         'form': form,
#         'account': account
#     })

@login_required
def transaction_create(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transaction_type = request.GET.get('type', 'deposit')
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            try:
                transaction = form.save(commit=False)
                transaction.account = account
                transaction.transaction_type = transaction_type
                
                # 잔액 계산
                amount = transaction.amount
                if transaction_type == 'withdrawal':
                    if account.balance < amount:
                        messages.error(request, '잔액이 부족합니다.')
                        return render(request, 'accounts/transaction_form.html', {'form': form, 'account': account})
                    account.balance -= amount
                else:
                    account.balance += amount
                
                # 거래 후 잔액 설정
                transaction.balance_after_transaction = account.balance
                
                # 저장
                account.save()
                transaction.save()
                
                messages.success(request, '거래가 성공적으로 기록되었습니다.')
                return redirect('accounts:account_transaction_list', pk=pk)
                
            except Exception as e:
                messages.error(request, f'거래 처리 중 오류가 발생했습니다: {str(e)}')
    else:
        form = TransactionForm()
    
    return render(request, 'accounts/transaction_form.html', {
        'form': form,
        'account': account
    })

def transaction_api(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.transactions.all().order_by('-transaction_date')
    
    transactions_data = [{
        'transaction_date': transaction.transaction_date,
        'transaction_type': transaction.transaction_type,
        'amount': str(transaction.amount),
        'balance_after_transaction': str(transaction.balance_after_transaction),
        'description': transaction.description
    } for transaction in transactions]
    
    return JsonResponse({
        'transactions': transactions_data,
        'account_balance': str(account.balance)
    })


def transaction_list(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.transactions.all().order_by('-transaction_date')
    return render(request, 'accounts/transaction_list.html', {
        'account': account,
        'transactions': transactions
    })