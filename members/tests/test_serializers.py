# from unittest.mock import patch
#
# from rest_framework.test import APITestCase
#
# from members.models import User
# from members.serializers import (
#     AddressValidationSerializer,
#     CompanyRegisterSerializer,
#     LoginSerializer,
#     UserRegisterSerializer,
# )
#
#
# class SerializerTestCase(APITestCase):
#
#     def setUp(self):
#         self.valid_user_data = {
#             "email": "testuser@example.com",
#             "name": "Test User",
#             "password": "strongpassword",
#             "confirm_password": "strongpassword",
#             "address": "서울특별시 강남구",
#         }
#         self.invalid_user_data = {
#             "email": "",
#             "name": "",
#             "password": "weak",
#             "confirm_password": "notmatching",
#             "address": "",
#         }
#         self.valid_company_data = {
#             "email": "testcompany@example.com",
#             "name": "Test Company",
#             "password": "strongpassword",
#             "confirm_password": "strongpassword",
#             "phone_number": "010-1234-5678",
#             "company_url": "http://testcompany.com",
#             "address": "서울특별시 강남구",
#         }
#         self.invalid_company_data = {
#             "email": "",
#             "name": "",
#             "password": "weak",
#             "confirm_password": "notmatching",
#             "phone_number": "",
#             "company_url": "",
#             "address": "",
#         }
#
#     @patch("members.validators.validate_kakao_address")
#     def test_user_register_serializer_valid(self, mock_validate_kakao_address):
#         mock_validate_kakao_address.return_value = True
#         serializer = UserRegisterSerializer(data=self.valid_user_data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)
#
#     def test_user_register_serializer_invalid(self):
#         serializer = UserRegisterSerializer(data=self.invalid_user_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("email", serializer.errors)
#         self.assertIn("password", serializer.errors)
#
#     @patch("members.validators.validate_kakao_address")
#     def test_company_register_serializer_valid(self, mock_validate_kakao_address):
#         mock_validate_kakao_address.return_value = True
#         serializer = CompanyRegisterSerializer(data=self.valid_company_data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)
#
#     def test_company_register_serializer_invalid(self):
#         serializer = CompanyRegisterSerializer(data=self.invalid_company_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("email", serializer.errors)
#         self.assertIn("password", serializer.errors)
#
#     def test_login_serializer_valid_user(self):
#         user = User.objects.create_user(email="testuser@example.com", password="strongpassword")
#         data = {"email": "testuser@example.com", "password": "strongpassword", "user_type": "user"}
#         serializer = LoginSerializer(data=data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)
#
#     def test_login_serializer_invalid_user(self):
#         data = {"email": "invalid@example.com", "password": "wrongpassword", "user_type": "user"}
#         serializer = LoginSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#
#     @patch("members.validators.validate_kakao_address")
#     def test_address_validation_serializer_valid(self, mock_validate_kakao_address):
#         mock_validate_kakao_address.return_value = True
#         data = {"address": "서울특별시 강남구"}
#         serializer = AddressValidationSerializer(data=data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)
#
#     def test_address_validation_serializer_invalid(self):
#         data = {"address": ""}
#         serializer = AddressValidationSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
