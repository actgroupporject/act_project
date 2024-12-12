# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from members.models import User
#
#
# class APITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#         # Create a test user
#         self.user = User.objects.create_user(
#             email="user@test.com", password="password123", name="Test User", user_type="user", address="123 Test Street"
#         )
#
#         # Create a test company
#         self.company = User.objects.create_user(
#             email="company@test.com",
#             password="password123",
#             name="Test Company",
#             user_type="company",
#             address="서울특별시 강남구 테헤란로 123",
#         )
#
#     def test_user_registration(self):
#         data = {
#             "email": "user@test.com",
#             "name": "Test User",
#             "password": "password123",
#             "confirm_password": "password123",
#             "address": "서울특별시 강남구 테헤란로 123",  # 유효한 주소
#         }
#         response = self.client.post("/api/v1/accounts/user/register/", data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("message", response.data)
#         self.assertEqual(response.data["message"], "회원가입이 완료되었습니다. 로그인 해주세요.")
#
#     def test_user_registration_password_mismatch(self):
#         data = {
#             "email": "user@test.com",
#             "name": "Test User",
#             "password": "password123",
#             "confirm_password": "password123",
#             "address": "서울특별시 강남구 테헤란로 123",  # 유효한 주소
#         }
#         response = self.client.post("/api/v1/accounts/user/register/", data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("password", response.data)
#
#     def test_company_registration(self):
#         data = {
#             "email": "newcompany@test.com",
#             "name": "New Company",
#             "password": "password123",
#             "confirm_password": "password123",
#             "phone_number": "123-456-7890",
#             "company_url": "https://newcompany.com",
#             "address": "서울특별시 강남구 테헤란로 123",
#
#         }
#         response = self.client.post("/api/v1/accounts/company/register/", data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("message", response.data)
#         self.assertEqual(response.data["message"], "회원가입이 완료되었습니다. 로그인 해주세요.")
#
#     def test_login_user(self):
#         data = {
#             "email": "user@test.com",
#             "password": "password123",
#             "user_type": "user",
#         }
#         response = self.client.post("/api/v1/accounts/login/", data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("message", response.data)
#         self.assertEqual(response.data["message"], "Test User님, 환영합니다!")
#
#     def test_login_company(self):
#         data = {
#             "email": "company@test.com",
#             "password": "password123",
#             "user_type": "company",
#         }
#         response = self.client.post("/api/v1/accounts/login/", data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("message", response.data)
#         self.assertEqual(response.data["message"], "Test Company님, 환영합니다!")
#
#     def test_logout(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post("/api/v1/accounts/logout/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("message", response.data)
#         self.assertEqual(response.data["message"], "로그아웃되었습니다.")
