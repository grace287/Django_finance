from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.analysis_list, name='analysis_list'),
    path('api/', views.AnalysisListAPIView.as_view(), name='analysis_list_api'),
]