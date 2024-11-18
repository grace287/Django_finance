from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # username 필드 제거
    email = models.EmailField('이메일', unique=True)
    nickname = models.CharField('닉네임', max_length=30)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'users_customuser'  # 테이블 이름 명시적 지정
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return self.email