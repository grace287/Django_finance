from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('ANALYSIS', '분석 결과'),
        ('BALANCE', '잔액 알림'),
        ('TRANSACTION', '거래 알림'),
        ('SYSTEM', '시스템 알림'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='사용자'
    )
    notification_type = models.CharField('알림 유형', max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField('제목', max_length=200)
    message = models.TextField('내용')
    is_read = models.BooleanField('읽음 여부', default=False)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    read_at = models.DateTimeField('읽은 시간', null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = '알림'
        verbose_name_plural = '알림 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()