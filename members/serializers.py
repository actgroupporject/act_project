import requests  # type: ignore
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.serializers import (
    SocialLoginSerializer as BaseSocialLoginSerializer,
)
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .validators import validate_kakao_address


class SocialLoginSerializer(BaseSocialLoginSerializer):
    def validate(self, attrs):
        # 기존 검증 로직 호출
        data = super().validate(attrs)

        # 소셜 계정 검증
        social_account = self.get_social_account(data.get("id"))
        if social_account:
            data["social_account"] = social_account
        else:
            raise serializers.ValidationError("등록되지 않은 소셜 계정입니다. 먼저 회원가입을 진행해 주세요.")

        return data

    def get_social_account(self, uid):
        """주어진 uid에 해당하는 소셜 계정을 반환"""
        return SocialAccount.objects.filter(uid=uid).first()


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "confirm_password", "address", "user_type"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        if data.get("user_type") != "user":
            raise serializers.ValidationError({"user_type": "유효하지 않은 사용자 유형입니다."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        validated_data.pop("user_type", None)  # 제거
        user = User.objects.create_user(user_type="user", **validated_data)
        return user


class CompanyRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "confirm_password",
            "phone_number",
            "company_url",
            "address",
            "user_type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        if data.get("user_type") != "company":
            raise serializers.ValidationError({"user_type": "유효하지 않은 회사 유형입니다."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        validated_data.pop("user_type", None)  # 제거
        company = User.objects.create_user(user_type="company", **validated_data)
        return company

    # def create(self, validated_data):
    #     validated_data.pop("confirm_password")
    #     company = User.objects.create_user(user_type="company", **validated_data)
    #     return company


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=["user", "company"])

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user_type = data.get("user_type")

        # 사용자 유형에 따른 인증
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
        if user.user_type != user_type:
            raise serializers.ValidationError("사용자 유형이 일치하지 않습니다.")
        data["user"] = user
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    provider = serializers.ChoiceField(choices=["google", "facebook", "kakao"], required=False)
    access_token = serializers.CharField(required=False)  # 소셜 Access Token

    def validate(self, attrs):
        self.token = attrs["refresh"]
        self.provider = attrs.get("provider")
        self.access_token = attrs.get("access_token")
        try:
            RefreshToken(self.token)  # Refresh Token 유효성 검증
        except TokenError:
            raise serializers.ValidationError({"refresh": "Invalid or expired refresh token."})
        return attrs

    def save(self, **kwargs):
        # 1. Refresh Token 블랙리스트 처리
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()  # Refresh Token 블랙리스트 추가
        except Exception as e:
            raise serializers.ValidationError("An error occurred while blacklisting the token.")

        # 2. 소셜 로그아웃 처리 (선택)
        if self.provider and self.access_token:
            self.perform_social_logout(self.provider, self.access_token)

    def perform_social_logout(self, provider, access_token):
        """
        소셜 로그아웃 처리 함수
        """
        if provider == "google":
            self.google_logout(access_token)
        elif provider == "facebook":
            self.facebook_logout(access_token)
        elif provider == "kakao":
            self.kakao_logout(access_token)

    def google_logout(self, access_token):

        revoke_url = "https://oauth2.googleapis.com/revoke"
        response = requests.post(revoke_url, params={"token": access_token})
        if response.status_code != 200:
            raise serializers.ValidationError({"google": "Failed to revoke Google session."})

    def facebook_logout(self, access_token):
        import requests

        logout_url = "https://www.facebook.com/logout.php"
        response = requests.get(logout_url, params={"access_token": access_token})
        if response.status_code != 200:
            raise serializers.ValidationError({"facebook": "Failed to revoke Facebook session."})

    def kakao_logout(self, access_token):
        import requests

        logout_url = "https://kapi.kakao.com/v1/user/logout"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(logout_url, headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError({"kakao": "Failed to revoke Kakao session."})


class AddressValidationSerializer(serializers.Serializer):
    address = serializers.CharField()

    def validate_address(self, value):
        # validate_kakao_address 호출
        if not value or not validate_kakao_address(value):
            raise serializers.ValidationError("유효하지 않은 주소입니다.")
        return value
