import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from members.models import Company

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
User = get_user_model()


class UserRegistrationTestCase(TestCase):
    def test_user_register_success(self):
        # 유저 회원가입 테스트
        response = self.client.post(
            reverse("user_register"),
            {
                "email": "testuser@example.com",
                "name": "Test User",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())  # 유저 생성 확인

    def test_user_register_password_mismatch(self):
        # 비밀번호 틀린 가입실패 테스트
        response = self.client.post(
            reverse("user_register"),
            {
                "email": "testuser@example.com",
                "name": "Test User",
                "password": "password123",
                "confirm_password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertFalse(User.objects.filter(email="testuser@example.com").exists())  # 유저 생성되지 않음


class CompanyRegistrationTestCase(TestCase):
    def test_company_register_success(self):
        # 회사 가입 테스트
        response = self.client.post(
            reverse("company_register"),
            {
                "email": "testcompany@example.com",
                "name": "Test Company",
                "password": "password123",
                "confirm_password": "password123",
                "phone_number": "123456789",
                "company_url": "http://example.com",
            },
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertTrue(Company.objects.filter(email="testcompany@example.com").exists())  # 회사 생성 확인

    def test_company_register_password_mismatch(self):
        # 회원가입 실패 테스트
        response = self.client.post(
            reverse("company_register"),
            {
                "email": "testcompany@example.com",
                "name": "Test Company",
                "password": "password123",
                "confirm_password": "wrongpassword",
                "phone_number": "123456789",
                "company_url": "http://example.com",
            },
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertFalse(Company.objects.filter(email="testcompany@example.com").exists())  # 회사 생성되지 않음


class LoginTestCase(TestCase):
    def setUp(self):
        # 성공 테스트
        self.user = User.objects.create_user(email="user@example.com", name="Test User", password="password123")
        self.company = Company.objects.create_user(
            email="company@example.com", name="Test Company", password="password123", phone_number="123456789"
        )

    def test_user_login_success(self):
        # 유저 로그인 성공 테스트
        response = self.client.post(
            reverse("login"),
            {"email": "user@example.com", "password": "password123", "user_type": "user"},
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertRedirects(response, reverse("user_home"))  # 유저 홈 리다이렉트 확인

    def test_company_login_success(self):
        # 회사 로그인 성공 테스트
        response = self.client.post(
            reverse("login"),
            {"email": "company@example.com", "password": "password123", "user_type": "company"},
        )
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertRedirects(response, reverse("company_home"))  # 회사 홈 리다이렉트 확인

    def test_login_invalid_credentials(self):
        # 실패 테스트
        response = self.client.post(
            reverse("login"),
            {"email": "wrong@example.com", "password": "wrongpassword", "user_type": "user"},
        )
        self.assertEqual(response.status_code, 200)  # 로그인 실패 시 동일 페이지 반환
        self.assertContains(response, "이메일 또는 비밀번호가 올바르지 않습니다.")


class LogoutTestCase(TestCase):
    def setUp(self):
        # 유저 생성
        self.user = User.objects.create_user(email="user@example.com", name="Test User", password="password123")
        self.client.login(email="user@example.com", password="password123")

    def test_logout(self):
        # 로그아웃 성공
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # 리다이렉트 확인
        self.assertRedirects(response, reverse("login"))  # 로그인 페이지 리다이렉트 확인
