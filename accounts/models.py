from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from .validators import validate_strong_password


class UserManager(BaseUserManager):
    def create_user(self, email, student_id, name, major, password=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')

        email = self.normalize_email(email)

        if not email.endswith('@dankook.ac.kr'):
            raise ValueError('이메일은 반드시 단국대학교 이메일을 사용해야 합니다.')

        if password:
            validate_strong_password(password)

        user = self.model(
            email=email,
            student_id=student_id,
            name=name,
            major=major
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, student_id, name, major, password=None):
        user = self.create_user(email, student_id, name, major, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    MAJOR_CHOICES = [
        ("IBA", "International Business Administration"),
        ("MSE", "Mobile Systems Engineering"),
        ("BME", "Bio and Material Engineering"),
        ("KST", "Korea Studies"),
        ("AFM", "Acting & Filmmaking"),
        ("GCE", "Global Core Education"),
    ]

    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=8)
    name = models.CharField(max_length=30)
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_id', 'name', 'major']

    def __str__(self):
        return self.email


class BuddyProfile(models.Model):
    INTEREST_CHOICES = [
        ("sports", "운동"),
        ("games", "게임"),
        ("music", "음악"),
        ("pets", "반려동물"),
        ("travel", "여행"),
        ("food", "음식"),
        ("anime", "애니"),
        ("study", "공부"),
    ]

    LANGUAGE_CHOICES = [
        ("korean", "한국어"),
        ("english", "영어"),
        ("chinese", "중국어"),
        ("japanese", "일본어"),
        ("french", "프랑스어"),
        ("spanish", "스페인어"),
    ]

    PURPOSE_CHOICES = [
        ("friendship", "친구 사귀기"),
        ("language", "언어 교환"),
        ("culture", "문화 체험"),
    ]

    MATCHING_TYPE_CHOICES = [
        ("1:1", "1:1"),
        ("N:N", "N:N"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buddy_profile')
    interest = models.CharField(max_length=200)  
    language = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    matching_type = models.CharField(max_length=3, choices=MATCHING_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.email}의 버디 프로필"


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {'인증됨' if self.is_verified else '미인증'}"
