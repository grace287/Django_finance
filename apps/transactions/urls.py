from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_home, name='transaction_list'),  # 전체 거래내역
    path('<int:pk>/transactions/', views.account_transaction_list, name='account_transaction_list'),  # 특정 계좌의 거래내역
    path('<int:pk>/transactions/create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/transactions/api/', views.transaction_api, name='transaction_api'),
]