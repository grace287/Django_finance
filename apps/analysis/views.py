from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.models import Account, Transaction

def analysis_list(request):
    accounts = Account.objects.filter(user=request.user)
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 전체 통계
    all_transactions = Transaction.objects.filter(
        account__user=request.user,
        transaction_date__gte=month_start
    )
    
    total_stats = {
        'total_balance': sum(account.balance for account in accounts),
        'total_deposits': all_transactions.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_withdrawals': all_transactions.filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_transactions': all_transactions.count()
    }
    
    context = {
        'accounts': accounts,
        'total_stats': total_stats,
    }
    
    return render(request, 'analysis/analysis_list.html', context)

class AnalysisListAPIView(APIView):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        all_transactions = Transaction.objects.filter(
            account__user=request.user,
            transaction_date__gte=month_start
        )
        
        data = {
            'total_balance': sum(account.balance for account in accounts),
            'total_deposits': all_transactions.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_withdrawals': all_transactions.filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_transactions': all_transactions.count(),
            'accounts': []
        }
        
        for account in accounts:
            monthly_stats = account.get_monthly_stats()
            account_data = {
                'id': account.id,
                'bank_name': account.get_bank_code_display(),
                'account_number': account.account_number,
                'balance': float(account.balance),
                'monthly_deposits': float(monthly_stats['deposits']),
                'monthly_withdrawals': float(monthly_stats['withdrawals']),
                'monthly_transactions': monthly_stats['count'],
                'recent_transactions': []
            }
            
            for transaction in account.get_recent_transactions():
                account_data['recent_transactions'].append({
                    'date': transaction.transaction_date,
                    'type': transaction.transaction_type,
                    'amount': float(transaction.amount),
                    'balance': float(transaction.balance_after_transaction),
                    'description': transaction.description
                })
            
            data['accounts'].append(account_data)
        
        return Response(data)