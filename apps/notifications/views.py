from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, '알림을 읽음으로 표시했습니다.')
    return redirect('notifications:notification_list')

@login_required
def notification_read_all(request):
    Notification.objects.filter(user=request.user, is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    messages.success(request, '모든 알림을 읽음으로 표시했습니다.')
    return redirect('notifications:notification_list')

@login_required
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    
    messages.success(request, '알림이 삭제되었습니다.')
    return redirect('notifications:notification_list')