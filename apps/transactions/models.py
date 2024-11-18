from django.db import models
from django.conf import settings
from apps.accounts.models import Account

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('deposit', '입금'),
        ('withdrawal', '출금'),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',  # related_name 변경
        verbose_name='계좌'
    )
    transaction_type = models.CharField('거래유형', max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField('금액', max_digits=15, decimal_places=2)
    description = models.CharField('설명', max_length=200)
    transaction_date = models.DateTimeField('거래일시', auto_now_add=True)
    balance_after_transaction = models.DecimalField(
        '거래 후 잔액',
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = '거래'
        verbose_name_plural = '거래 목록'

    # def __str__(self):
    #     return f"{self.get_transaction_type_display()} - {self.amount}"

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         account = self.account
    #         if self.transaction_type == 'deposit':
    #             account.balance += self.amount
    #         else:
    #             account.balance -= self.amount
    #         self.balance_after_transaction = account.balance
    #         account.save()
    #     super().save(*args, **kwargs)