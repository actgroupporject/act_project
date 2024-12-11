from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now

from .validators import validate_kakao_address


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 항목입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("user", "User"),
        ("company", "Company"),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="user")
    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=50, verbose_name="이름")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, verbose_name="전화번호", blank=True)
    address = models.CharField(max_length=255, verbose_name="주소", blank=True, validators=[validate_kakao_address])
    description = models.TextField(blank=True, null=True, verbose_name="설명")
    portfolio = models.FileField(upload_to="portfolios/", null=True, blank=True, verbose_name="포트폴리오")
    birthday = models.DateField(null=True, blank=True, verbose_name="생일")
    company_url = models.URLField(max_length=256, blank=True, null=True, verbose_name="화사 URL")
    date_joined = models.DateTimeField(default=now, verbose_name="가입일")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def __str__(self):
        return self.email
