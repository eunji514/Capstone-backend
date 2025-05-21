from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from .validators import validate_strong_password


class UserManager(BaseUserManager):
    def create_user(self, email, student_id, name, major, password=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')

        email = self.normalize_email(email)

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
