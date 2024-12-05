from django.core.exceptions import ValidationError
from django.test import TestCase

from members.models import Company, User


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "testpassword123",
            "gender": "M",
            "phone_number": "01012345678",
            "height": 175.5,
            "weight": 70.2,
            "self_introduced": "Hello, I am a test user.",
            "birthday": "1995-01-01",
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.name, self.user_data["name"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="adminpassword")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["email"])

    def test_user_email_is_unique(self):
        User.objects.create_user(**self.user_data)
        with self.assertRaises(ValidationError):
            User.objects.create_user(**self.user_data)


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company_data = {
            "email": "testcompany@example.com",
            "name": "Test Company",
            "password": "testpassword123",
            "phone_number": "0212345678",
            "company_url": "http://www.testcompany.com",
            "description": "We are a test company.",
        }

    def test_create_company(self):
        company = Company.objects.create_user(**self.company_data)
        self.assertEqual(company.email, self.company_data["email"])
        self.assertEqual(company.name, self.company_data["name"])
        self.assertTrue(company.is_active)
        self.assertFalse(company.is_staff)

    def test_create_superuser_company(self):
        supercompany = Company.objects.create_superuser(email="admincompany@example.com", password="adminpassword")
        self.assertTrue(supercompany.is_staff)
        self.assertTrue(supercompany.is_superuser)

    def test_company_string_representation(self):
        company = Company.objects.create_user(**self.company_data)
        self.assertEqual(str(company), self.company_data["name"])

    def test_company_email_is_unique(self):
        Company.objects.create_user(**self.company_data)
        with self.assertRaises(ValidationError):
            Company.objects.create_user(**self.company_data)
