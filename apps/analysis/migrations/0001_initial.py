# Generated by Django 5.1.3 on 2024-11-18 17:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(choices=[('expense', '지출'), ('income', '수입')], max_length=10, verbose_name='분석 대상')),
                ('type', models.CharField(choices=[('weekly', '주간'), ('monthly', '월간')], max_length=10, verbose_name='분석 유형')),
                ('period_start', models.DateField(verbose_name='시작일')),
                ('period_end', models.DateField(verbose_name='종료일')),
                ('description', models.TextField(verbose_name='설명')),
                ('result_image', models.ImageField(upload_to='analysis/%Y/%m/', verbose_name='결과 이미지')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '분석',
                'verbose_name_plural': '분석 목록',
                'db_table': 'analysis_analysis',
            },
        ),
    ]
