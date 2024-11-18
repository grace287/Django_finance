
from django import forms
from .models import Account

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type']
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-control'}),
        }

class AccountCreateForm(forms.ModelForm):
    initial_balance = forms.DecimalField(
        label='초기 입금액',
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ['bank_code', 'account_number', 'account_type', 'balance']
        labels = {
            'bank_code': '은행',
            'account_number': '계좌번호',
            'account_type': '계좌유형',
            'balance': '초기잔액',
        }
        widgets = {
            'bank_code': forms.Select(attrs={'class': 'form-select'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-select'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_initial_balance(self):
        initial_balance = self.cleaned_data.get('initial_balance')
        if initial_balance < 0:
            raise forms.ValidationError('초기 입금액은 0원 이상이어야 합니다.')
        return initial_balance