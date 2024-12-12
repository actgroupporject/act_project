# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError
# from members.serializers import (
#     SocialLoginSerializer,
#     UserRegisterSerializer,
#     CompanyRegisterSerializer,
#     LoginSerializer,
#     AddressValidationSerializer,
# )
# from allauth.socialaccount.models import SocialAccount
#
#
# class SerializerTestCase(TestCase):
#     def setUp(self):
#         self.user_model = get_user_model()
#
#         # 일반 사용자 생성
#         self.user = self.user_model.objects.create_user(
#             email="user@test.com",
#             password="password123",
#             name="Test User",
#             user_type="user",
#             address="123 Test Street"
#         )
#
#         # 회사 사용자 생성
#         self.company = self.user_model.objects.create_user(
#             email="company@test.com",
#             password="password123",
#             name="Test Company",
#             user_type="company",
#             address="456 Test Avenue"
#         )
#
#         # 소셜 계정 생성
#         self.social_account = SocialAccount.objects.create(
#             user=self.user,
#             uid="social_uid",
#             provider="google"
#         )
#
#     def test_user_register_serializer_valid(self):
#         data = {
#             "email": "newuser@test.com",
#             "name": "New User",
#             "password": "password123",
#             "confirm_password": "password123",
#             "address": "789 New Street",
#         }
#         serializer = UserRegisterSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         user = serializer.save()
#         self.assertEqual(user.email, "newuser@test.com")
#         self.assertEqual(user.user_type, "user")
#
#     def test_user_register_serializer_password_mismatch(self):
#         data = {
#             "email": "newuser@test.com",
#             "name": "New User",
#             "password": "password123",
#             "confirm_password": "wrongpassword",
#             "address": "789 New Street",
#         }
#         serializer = UserRegisterSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("password", serializer.errors)
#
#     def test_company_register_serializer_valid(self):
#         data = {
#             "email": "newcompany@test.com",
#             "name": "New Company",
#             "password": "password123",
#             "confirm_password": "password123",
#             "phone_number": "123-456-7890",
#             "company_url": "https://newcompany.com",
#             "address": "999 Company Blvd",
#         }
#         serializer = CompanyRegisterSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         company = serializer.save()
#         self.assertEqual(company.email, "newcompany@test.com")
#         self.assertEqual(company.user_type, "company")
#
#     def test_company_register_serializer_password_mismatch(self):
#         data = {
#             "email": "newcompany@test.com",
#             "name": "New Company",
#             "password": "password123",
#             "confirm_password": "wrongpassword",
#             "phone_number": "123-456-7890",
#             "company_url": "https://newcompany.com",
#             "address": "999 Company Blvd",
#         }
#         serializer = CompanyRegisterSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("password", serializer.errors)
#
#     def test_login_serializer_valid_user(self):
#         data = {
#             "email": "user@test.com",
#             "password": "password123",
#             "user_type": "user",
#         }
#         serializer = LoginSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         self.assertEqual(serializer.validated_data["user"], self.user)
#
#     def test_login_serializer_invalid_user(self):
#         data = {
#             "email": "wrong@test.com",
#             "password": "wrongpassword",
#             "user_type": "user",
#         }
#         serializer = LoginSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("non_field_errors", serializer.errors)
#
#     def test_social_login_serializer_valid(self):
#         data = {"id": "social_uid"}
#         serializer = SocialLoginSerializer(data=data)
#         serializer.is_valid()
#         self.assertEqual(serializer.validated_data["social_account"], self.social_account)
#
#     def test_social_login_serializer_invalid(self):
#         data = {"id": "invalid_uid"}
#         serializer = SocialLoginSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("non_field_errors", serializer.errors)
#
#     def test_address_validation_serializer_valid(self):
#         data = {"address": "123 Valid Address"}
#         serializer = AddressValidationSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#
#     def test_address_validation_serializer_invalid(self):
#         data = {"address": ""}
#         serializer = AddressValidationSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("address", serializer.errors)
