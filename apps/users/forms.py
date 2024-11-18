from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일 주소를 입력하세요'
        })
    )
    nickname = forms.CharField(
        label='닉네임',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '닉네임을 입력하세요'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 다시 입력하세요'
        })

    def save(self, commit=True):
        # 사용자 객체 생성
        user = super().save(commit=False)
        # username 필드에 email 값을 기본으로 설정
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user