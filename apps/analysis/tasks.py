from celery import shared_task
from django.contrib.auth import get_user_model
from .analyzers import TransactionAnalyzer

User = get_user_model()

@shared_task
def analyze_weekly_transactions():
    for user in User.objects.all():
        analyzer = TransactionAnalyzer(user, 'weekly', 'expense')
        analyzer.analyze()
        analyzer = TransactionAnalyzer(user, 'weekly', 'income')
        analyzer.analyze()

@shared_task
def analyze_monthly_transactions():
    for user in User.objects.all():
        analyzer = TransactionAnalyzer(user, 'monthly', 'expense')
        analyzer.analyze()
        analyzer = TransactionAnalyzer(user, 'monthly', 'income')
        analyzer.analyze()