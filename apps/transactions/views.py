from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction
from apps.accounts.models import Account
from .forms import TransactionForm
from django.http import JsonResponse

@login_required
def transaction_home(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'accounts/transaction_home.html', {'accounts': accounts})

def account_transaction_list(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.account_transactions.all()
    return render(request, 'accounts/transaction_list.html', {
        'account': account,
        'transactions': transactions
    })

def transaction_detail(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        account__user=request.user
    )
    return render(request, 'accounts/transaction_detail.html', {
        'transaction': transaction
    })

def transaction_create(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            if transaction.transaction_type == 'withdrawal':
                if transaction.amount > account.balance:
                    messages.error(request, '잔액이 부족합니다.')
                    return render(request, 'accounts/transaction_form.html', {'form': form})
            transaction.save()
            messages.success(request, '거래가 성공적으로 기록되었습니다.')
            return redirect('accounts:account_transaction_list', pk=account.pk)
    else:
        transaction_type = request.GET.get('type', 'deposit')
        form = TransactionForm(initial={'transaction_type': transaction_type})
    
    return render(request, 'accounts/transaction_form.html', {
        'form': form,
        'account': account
    })

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        account__user=request.user
    )
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, '거래가 성공적으로 수정되었습니다.')
            return redirect('transactions:transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm(instance=transaction)
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
    
    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'title': '거래 수정',
        'transaction': transaction
    })

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        account__user=request.user
    )
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, '거래가 성공적으로 삭제되었습니다.')
        return redirect('transactions:transaction_list')
    
    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction
    })

def transaction_api(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')
    
    transactions_data = [{
        'transaction_date': transaction.transaction_date.isoformat(),
        'transaction_type': transaction.transaction_type,
        'amount': str(transaction.amount),
        'balance_after_transaction': str(transaction.balance_after_transaction),
        'description': transaction.description
    } for transaction in transactions]
    
    return JsonResponse({
        'transactions': transactions_data,
        'account_balance': str(account.balance)
    })