# Generated by Django 5.1.3 on 2024-11-18 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', '입금'), ('withdrawal', '출금')], max_length=10, verbose_name='거래유형')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='금액')),
                ('description', models.CharField(max_length=200, verbose_name='설명')),
                ('transaction_date', models.DateTimeField(auto_now_add=True, verbose_name='거래일시')),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='거래 후 잔액')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account', verbose_name='계좌')),
            ],
            options={
                'verbose_name': '거래',
                'verbose_name_plural': '거래 목록',
                'ordering': ['-transaction_date'],
            },
        ),
    ]
