import logging

import requests  # type: ignore
from allauth.socialaccount.providers.google.views import (  # type: ignore
    GoogleOAuth2Adapter,
)
from allauth.socialaccount.providers.kakao.views import (  # type: ignore
    KakaoOAuth2Adapter,
)
from allauth.socialaccount.providers.naver.views import (  # type: ignore
    NaverOAuth2Adapter,
)
from allauth.socialaccount.providers.oauth2.client import OAuth2Client  # type: ignore
from decouple import config
from dj_rest_auth.registration.views import (
    SocialLoginView as BaseSocialLoginView,  # type: ignore
)
from django.contrib.auth import (  # type: ignore
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (  # type: ignore
    CompanyRegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    SocialLoginSerializer,
    UserRegisterSerializer,
)


@extend_schema(
    request=UserRegisterSerializer,  # 요청 Serializer
    responses={201: {"message": "회원가입이 완료되었습니다."}},  # 응답 예시
)
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다. 로그인 해주세요."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserRegisterSerializer,  # 요청 Serializer
    responses={201: {"message": "회원가입이 완료되었습니다."}},  # 응답 예시
)
class CompanyRegisterAPIView(APIView):
    def post(self, request):
        serializer = CompanyRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다. 로그인 해주세요."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,  # 요청 Serializer
    responses={201: {"message": "로그인이 완료되었습니다."}},
)
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            user_type = request.data.get("user_type")

            # Django login
            login(request, user)

            # 사용자 유형에 따른 메시지
            if user_type == "user":
                return Response({"message": f"{user.name}님, 환영합니다!"}, status=status.HTTP_200_OK)
            elif user_type == "company":
                return Response({"message": f"{user.name}님, 환영합니다!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LogoutSerializer,  # 요청 Serializer
    responses={201: {"message": "로그아웃이 완료되었습니다."}},
)
# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         if serializer.is_valid():
#             logout(request)
#             return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    통합 로그아웃 뷰
    - 일반 JWT 로그아웃
    - 소셜 로그아웃
    """

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Django 세션 로그아웃 처리
            logout(request)
            return Response({"message": "로그아웃이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialLoginView(BaseSocialLoginView):
    """
    공통 소셜 로그인 View
    """

    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


"""
    구글 소셜 로그인
"""

logger = logging.getLogger(__name__)


class GoogleLoginView(APIView):
    """
    Google 소셜 로그인 시작
    """

    def get(self, request, *args, **kwargs):
        google_authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        client_id = config("GOOGLE_CLIENT_ID")
        redirect_uri = config("GOOGLE_REDIRECT_URI")
        scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"
        state = request.session.session_key or "random_state_value"
        url = (
            f"{google_authorize_url}?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            f"&state={state}"
        )
        return redirect(url)


class GoogleCallbackView(APIView):
    """
    Google 소셜 회원가입 및 로그인 처리
    """

    def get(self, request, *args, **kwargs):
        # 1. Authorization Code 가져오기
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code:
            return Response({"error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Access Token 및 Refresh Token 요청
        access_token, refresh_token = self.exchange_code_for_token(code, state)
        if not access_token:
            return Response({"error": "Failed to fetch tokens from Google"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Access Token으로 사용자 정보 가져오기
        user_info = self.get_user_info(access_token)
        if not user_info:
            return Response({"error": "Failed to fetch user info from Google"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Fetched User Info: {user_info}")

        # 4. 사용자 생성 또는 가져오기
        user = self.get_or_create_user(user_info)

        # 5. JWT 토큰 발급
        jwt_tokens = self.generate_jwt(user)

        # 6. JWT 및 소셜 토큰 반환
        return Response(
            {
                "jwt": jwt_tokens,
                "social_tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token or "Google does not always provide refresh tokens",
                },
            },
            status=status.HTTP_200_OK,
        )

    def exchange_code_for_token(self, code, state):
        """
        Google에서 Access Token 및 Refresh Token 가져오기
        """
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": config("GOOGLE_CLIENT_ID"),
            "client_secret": config("GOOGLE_SECRET"),
            "redirect_uri": config("GOOGLE_REDIRECT_URI"),
            "code": code,
        }
        response = requests.post(token_url, data=data)

        logger.info(f"Token Request Data: {data}")
        logger.info(f"Token Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            tokens = response.json()
            return tokens.get("access_token"), tokens.get("refresh_token")
        return None, None

    def get_user_info(self, access_token):
        """
        Access Token을 사용하여 Google 사용자 정보 가져오기
        """
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)

        logger.info(f"User Info Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return response.json()
        return None

    def get_or_create_user(self, user_info):
        """
        사용자 정보로 User 생성 또는 가져오기
        """
        User = get_user_model()
        email = user_info.get("email")
        if not email:
            raise ValueError("Google 계정에서 이메일을 가져올 수 없습니다.")

        name = user_info.get("name", "익명 사용자")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "user_type": "user",
                "is_active": True,
            },
        )
        return user

    def generate_jwt(self, user):
        """
        JWT 토큰 생성
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


"""
    카카오 소셜 로그인
"""


class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/api/v1/accounts/kakao/callback/"

    def get(self, request, *args, **kwargs):
        kakao_authorize_url = "https://kauth.kakao.com/oauth/authorize"
        client_id = config("KAKAO_CLIENT_ID")
        redirect_uri = self.callback_url
        return redirect(f"{kakao_authorize_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")


class KakaoCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. Authorization Code 가져오기
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Authorization Code로 Access Token 및 Refresh Token 요청
        access_token, refresh_token = self.exchange_code_for_token(code)
        if not access_token:
            return Response({"error": "Failed to fetch tokens from Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Access Token으로 사용자 정보 가져오기
        user_info = self.get_user_info(access_token)
        if not user_info:
            return Response({"error": "Failed to fetch user info from Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. 사용자 생성 또는 가져오기
        user = self.get_or_create_user(user_info)

        # 5. JWT 발급
        jwt_tokens = self.generate_jwt(user)

        # 6. 응답 반환
        return Response(
            {
                "jwt": jwt_tokens,
                "social_tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token or "Not provided by Kakao",
                },
            },
            status=status.HTTP_200_OK,
        )

    def exchange_code_for_token(self, code):
        """
        Kakao API를 통해 Access Token 및 Refresh Token 요청
        """
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": config("KAKAO_CLIENT_ID"),
            "client_secret": config("KAKAO_SECRET"),
            "redirect_uri": config("KAKAO_REDIRECT_URI"),
            "code": code,
        }
        response = requests.post(token_url, data=data)

        # 요청 실패 처리
        if response.status_code != 200:
            return None, None

        tokens = response.json()
        return tokens.get("access_token"), tokens.get("refresh_token")

    def get_user_info(self, access_token):
        """
        Kakao API를 통해 사용자 정보 가져오기
        """
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)

        # 요청 실패 처리
        if response.status_code != 200:
            return None

        return response.json()

    def get_or_create_user(self, user_info):
        """
        소셜 로그인 시 사용자 생성 또는 가져오기
        """
        User = get_user_model()  # Custom User 모델 가져오기

        # 이메일 가져오기, 없으면 기본값 설정
        email = user_info.get("kakao_account", {}).get("email", None)
        if not email:
            email = f"anonymous_{user_info.get('id')}@kakao.com"

        # 닉네임 가져오기
        name = user_info.get("properties", {}).get("nickname", "익명 사용자")

        # 사용자 생성 또는 가져오기
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "user_type": "user",  # 기본값 설정
                "is_active": True,
            },
        )
        return user

    def generate_jwt(self, user):
        """
        사용자에 대한 JWT 토큰 생성
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


"""
    네이버 소셜 로그인
"""


class NaverLoginView(APIView):
    """
    Naver 소셜 로그인 뷰 (사용자 인증 요청)
    """

    def get(self, request, *args, **kwargs):
        naver_authorize_url = "https://nid.naver.com/oauth2.0/authorize"
        client_id = config("NAVER_CLIENT_ID")
        redirect_uri = config("NAVER_REDIRECT_URI")
        state = request.session.session_key or "random_state_value"
        url = (
            f"{naver_authorize_url}?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
        )
        return redirect(url)


class NaverCallbackView(APIView):
    """
    Naver 소셜 회원가입 및 로그인 처리
    """

    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        # 1. Authorization Code 가져오기
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code:
            return Response({"error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Access Token 및 Refresh Token 요청
        access_token, refresh_token = self.exchange_code_for_token(code, state)
        if not access_token:
            return Response({"error": "Failed to fetch tokens from Naver"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Access Token으로 사용자 정보 가져오기
        user_info = self.get_user_info(access_token)
        if not user_info:
            return Response({"error": "Failed to fetch user info from Naver"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. 사용자 생성 또는 가져오기
        user = self.get_or_create_user(user_info)

        # 5. JWT 토큰 발급
        jwt_tokens = self.generate_jwt(user)

        # 6. JWT 및 소셜 토큰 반환
        return Response(
            {
                "jwt": jwt_tokens,
                "social_tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token or "Naver does not provide refresh tokens",
                },
            },
            status=status.HTTP_200_OK,
        )

    def exchange_code_for_token(self, code, state):
        """
        Naver에서 Access Token 및 Refresh Token 가져오기
        """
        token_url = "https://nid.naver.com/oauth2.0/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": config("NAVER_CLIENT_ID"),
            "client_secret": config("NAVER_SECRET"),
            "redirect_uri": config("NAVER_REDIRECT_URI"),
            "code": code,
            "state": state,
        }
        response = requests.post(token_url, data=data)

        logger.info(f"Token Request Data: {data}")
        logger.info(f"Token Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            tokens = response.json()
            return tokens.get("access_token"), tokens.get("refresh_token")
        return None, None

    def get_user_info(self, access_token):
        """
        Naver API를 사용하여 사용자 정보 가져오기
        """
        user_info_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)

        logger.info(f"User Info Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            user_data = response.json().get("response")
            if user_data:
                return user_data
        return None

    def get_or_create_user(self, user_info):
        """
        사용자 정보로 User 생성 또는 가져오기
        """
        User = get_user_model()
        email = user_info.get("email", f"anonymous_{user_info.get('id')}@naver.com")
        name = user_info.get("name", "익명 사용자")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "is_active": True,
            },
        )
        return user

    def generate_jwt(self, user):
        """
        JWT 토큰 생성
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
