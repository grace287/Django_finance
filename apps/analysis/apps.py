from django.apps import AppConfig

class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analysis'
    label = 'finance_analysis'  # 고유한 레이블 지정