from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                # 사용자 생성 및 저장
                user = form.save()
                
                # 백엔드를 명시적으로 지정하여 로그인
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                messages.success(request, '회원가입이 완료되었습니다.')
                print("회원가입 성공, 홈으로 리다이렉트")  # 디버깅용
                return redirect('users:home')
                
            except Exception as e:
                print(f"회원가입 중 오류 발생: {str(e)}")  # 디버깅용
                messages.error(request, '회원가입 중 오류가 발생했습니다.')
                
        else:
            # 폼 에러 메시지 출력
            print("폼 유효성 검사 실패:", form.errors)  # 디버깅용
            for field in form.errors:
                messages.error(request, f"{field}: {form.errors[field]}")
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '로그인되었습니다.')
            return redirect('users:home')
        else:
            messages.error(request, '이메일 또는 비밀번호가 올바르지 않습니다.')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('users:login')

def home_view(request):
    return render(request, 'users/home.html')