from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 관리자
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


# 사용자
class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        verbose_name="그룹",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True,
        verbose_name="권한",
    )

    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=50, verbose_name="이름")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 추가 필드
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], verbose_name="성별", blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="전화번호", blank=True)
    height = models.FloatField(default=0, verbose_name="키", blank=True)
    weight = models.FloatField(default=0, verbose_name="몸무게", blank=True)
    self_introduced = models.TextField(blank=True, null=True, verbose_name="자기소개")
    portfolio = models.BinaryField(null=True, verbose_name="포트폴리오")
    birthday = models.DateField(null=True, verbose_name="생일")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        verbose_name_plural = "유저들"

    def __str__(self):
        return self.email


# 회사
class Company(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_company_set",
        blank=True,
        verbose_name="그룹",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_company_permissions_set",
        blank=True,
        verbose_name="권한",
    )

    email = models.EmailField(unique=True, verbose_name="회사 이메일")
    name = models.CharField(max_length=50, verbose_name="회사 이름")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 추가 필드
    phone_number = models.CharField(max_length=15, verbose_name="회사 전화번호", blank=True)
    company_url = models.URLField(max_length=50, verbose_name="회사 홈페이지", blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="회사 설명")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "company"
        verbose_name = "회사"
        verbose_name_plural = "회사들"

    def __str__(self):
        return self.name
