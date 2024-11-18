from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_list, name='account_list'),
    path('create/', views.account_create, name='account_create'),
    path('<int:pk>/', views.account_detail, name='account_detail'),
    path('<int:pk>/update/', views.account_update, name='account_update'),
    path('<int:pk>/delete/', views.account_delete, name='account_delete'),
    
    # 거래내역 관련 URL 패턴
    path('transactions/', views.transaction_home, name='transaction_home'),
    path('<int:pk>/transactions/', views.transaction_list, name='account_transaction_list'),
    path('<int:pk>/transactions/create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/transactions/api/', views.transaction_api, name='transaction_api'),
]