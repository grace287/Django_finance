from django.db import models
from django.conf import settings


class Analysis(models.Model):
    ANALYSIS_TYPES = [
        ('weekly', '주간'),
        ('monthly', '월간'),
    ]
    
    ANALYSIS_ABOUT = [
        ('expense', '지출'),
        ('income', '수입'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='사용자'
    )
    about = models.CharField('분석 대상', max_length=10, choices=ANALYSIS_ABOUT)
    type = models.CharField('분석 유형', max_length=10, choices=ANALYSIS_TYPES)
    period_start = models.DateField('시작일')
    period_end = models.DateField('종료일')
    description = models.TextField('설명')
    result_image = models.ImageField('결과 이미지', upload_to='analysis/%Y/%m/')
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        db_table = 'analysis_analysis'
        verbose_name = '분석'
        verbose_name_plural = '분석 목록'