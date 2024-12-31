# 주소, 생년월일, 전화번호, 생년월일, 이메일, 휴대폰 번호, 주소,
import logging
import secrets

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
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

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
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout(request)
            return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)
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


class GoogleLoginView(BaseSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/api/v1/accounts/google/callback/"

    def get(self, request, *args, **kwargs):
        google_authorize_url = "https://accounts.google.com/o/oauth2/auth"
        client_id = config("GOOGLE_CLIENT_ID")
        redirect_uri = self.callback_url
        scope = "https://www.googleapis.com/auth/userinfo.email"
        state = "rando,_string"
        return redirect(
            f"{google_authorize_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}"
        )


class GoogleCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. 인증 코드 가져오기
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Authorization code is missing"}, status=400)

        # 2. 인증 코드로 접근 토큰 교환
        access_token = self.exchange_code_for_token(
            token_url="https://accounts.google.com/o/oauth2/token",
            client_id=config("GOOGLE_CLIENT_ID"),
            client_secret=config("GOOGLE_SECRET"),
            redirect_uri="http://127.0.0.1:8000/api/v1/accounts/google/callback/",
            code=code,
        )
        if not access_token:
            return JsonResponse({"error": "Failed to fetch access token from Google"}, status=400)

        # 3. 접근 토큰으로 사용자 정보 가져오기
        user_info = self.get_user_info(
            user_info_url="https://www.googleapis.com/oauth2/v2/userinfo", access_token=access_token
        )
        if not user_info:
            return JsonResponse({"error": "Failed to fetch user info from Google"}, status=400)

        # 4. 접근 토큰 반환
        return JsonResponse({"access_token": access_token, "user_info": user_info}, status=200)

    def exchange_code_for_token(self, token_url, client_id, client_secret, redirect_uri, code):
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    def get_user_info(self, user_info_url, access_token):
        # 접근 토큰으로 사용자 정보 요청
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None


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


logger = logging.getLogger(__name__)


class KakaoCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. 인증 코드 가져오기
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Authorization code is missing"}, status=400)

        # 2. 인증 코드로 접근 토큰 교환

        access_token = self.exchange_code_for_token(
            token_url="https://kauth.kakao.com/oauth/token",
            client_id=config("KAKAO_CLIENT_ID"),
            client_secret=config("KAKAO_SECRET"),
            redirect_uri="http://127.0.0.1:8000/api/v1/accounts/kakao/callback/",
            code=code,
        )
        if not access_token:
            return JsonResponse({"error": "Failed to fetch access token from Kakao"}, status=400)

        # 3. 접근 토큰으로 사용자 정보 가져오기
        user_info = self.get_user_info(user_info_url="https://kapi.kakao.com/v2/user/me", access_token=access_token)
        if not user_info:
            return JsonResponse({"error": "Failed to fetch user info from Kakao"}, status=400)

        # 3. 접근 토큰 반환
        logger.info(f"Access token successfully fetched: {access_token}")
        return JsonResponse({"access_token": access_token, "user_info": user_info}, status=200)

    def exchange_code_for_token(self, token_url, client_id, client_secret, redirect_uri, code):
        # 인증 코드를 접근 토큰으로 교환
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        response = requests.post(token_url, data=data)

        # 요청 및 응답 로그
        logger.info(f"Kakao token request payload: {data}")
        logger.info(f"Kakao token response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return response.json().get("access_token")
        logger.error(f"Token exchange failed: {response.json()}")
        return None

    def get_user_info(self, user_info_url, access_token):
        # 접근 토큰으로 사용자 정보 요청
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None


"""
    네이버 소셜 로그인
"""


class NaverLoginView(BaseSocialLoginView):
    adapter_class = NaverOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/api/v1/accounts/naver/callback/"

    def get(self, request, *args, **kwargs):
        naver_authorize_url = "https://nid.naver.com/oauth2.0/authorize"
        client_id = config("GOOGLE_CLIENT_ID")
        redirect_uri = self.callback_url
        state = secrets.token_urlsafe(16)  # CSRF 방지를 위한 상태 값
        authorization_url = (
            f"{naver_authorize_url}?client_id={client_id}"
            f"&redirect_uri={redirect_uri}&response_type=code&state={state}"
        )

        return redirect(authorization_url)


class NaverCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. 인증 코드 가져오기
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Authorization code is missing"}, status=400)

        # 2. 인증 코드로 접근 토큰 교환
        access_token = self.exchange_code_for_token(
            token_url="https://nid.naver.com/oauth2.0/token",
            client_id=config("GOOGLE_CLIENT_ID"),
            client_secret=config("GOOGLE_SECRET"),
            redirect_uri="http://127.0.0.1:8000/api/v1/accounts/naver/callback/",
            code=code,
        )
        if not access_token:
            return JsonResponse({"error": "Failed to fetch access token from Naver"}, status=400)

        # 3. 접근 토큰으로 사용자 정보 가져오기
        user_info = self.get_user_info(user_info_url="https://openapi.naver.com/v1/nid/me", access_token=access_token)
        if not user_info:
            return JsonResponse({"error": "Failed to fetch user info from Naver"}, status=400)

        return JsonResponse({"access_token": access_token, "user_info": user_info}, status=200)

    def exchange_code_for_token(self, token_url, client_id, client_secret, redirect_uri, code):
        # 인증 코드를 접근 토큰으로 교환
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    def get_user_info(self, user_info_url, access_token):
        # 접근 토큰으로 사용자 정보 요청
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
