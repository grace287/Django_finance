# Generated by Django 5.1.3 on 2024-11-18 17:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_code', models.CharField(choices=[('KB', 'KB국민은행'), ('SH', '신한은행'), ('WR', '우리은행'), ('NH', '농협은행'), ('KK', '카카오뱅크')], max_length=20)),
                ('account_number', models.CharField(max_length=50)),
                ('account_type', models.CharField(choices=[('SAVINGS', '예금'), ('CHECKING', '입출금'), ('CREDIT', '신용카드')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', '입금'), ('withdrawal', '출금')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.CharField(max_length=100)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_transactions', to='accounts.account')),
            ],
        ),
    ]
