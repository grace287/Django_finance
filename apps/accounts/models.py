from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

class Account(models.Model):
    BANK_CHOICES = [
        ('KB', 'KB국민은행'),
        ('SH', '신한은행'),
        ('WR', '우리은행'),
        ('NH', '농협은행'),
        ('KK', '카카오뱅크'),
    ]
    
    ACCOUNT_TYPES = [
        ('SAVINGS', '예금'),
        ('CHECKING', '입출금'),
        ('CREDIT', '신용카드'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_code = models.CharField(max_length=20, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_bank_code_display()} - {self.account_number}"

    def get_monthly_stats(self):
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        transactions = self.account_transactions.filter(transaction_date__gte=month_start)
        
        return {
            'deposits': transactions.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0,
            'withdrawals': transactions.filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0,
            'count': transactions.count()
        }

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', '입금'),
        ('withdrawal', '출금'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)