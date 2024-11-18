import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Analysis
from apps.transactions.models import Transaction

class TransactionAnalyzer:
    def __init__(self, user, analysis_type, about):
        self.user = user
        self.analysis_type = analysis_type
        self.about = about
        
    def analyze(self):
        # 기간 설정
        if self.analysis_type == 'weekly':
            period_start = datetime.now() - timedelta(days=7)
            period_end = datetime.now()
        else:  # monthly
            period_start = datetime.now() - timedelta(days=30)
            period_end = datetime.now()
            
        # 데이터 가져오기
        transactions = Transaction.objects.filter(
            account__user=self.user,
            transaction_date__range=(period_start, period_end)
        )
        
        # Pandas DataFrame 생성
        df = pd.DataFrame(list(transactions.values()))
        
        # 그래프 생성
        plt.figure(figsize=(10, 6))
        # ... 그래프 생성 로직 ...
        
        # 이미지로 저장
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_file = ContentFile(buffer.getvalue())
        
        # Analysis 모델 생성
        analysis = Analysis.objects.create(
            user=self.user,
            about=self.about,
            type=self.analysis_type,
            period_start=period_start,
            period_end=period_end,
            description=self.generate_description(df)
        )
        analysis.result_image.save(f'analysis_{datetime.now()}.png', image_file)
        
        return analysis