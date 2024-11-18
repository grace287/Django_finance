from .models import Notification

def create_notification(user, notification_type, title, message):
    """
    알림을 생성하는 유틸리티 함수
    """
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message
    )