from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned

from .models import User


class UserBackend(ModelBackend):
    """
    일반 사용자(User) 인증을 처리하는 백엔드
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            # 이메일을 통해 사용자 검색
            user = User.objects.get(email=email, user_type="user")
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None  # 동일한 이메일의 중복 데이터가 있는 경우
        return None


class CompanyBackend(ModelBackend):
    """
    회사 사용자(Company) 인증을 처리하는 백엔드
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            # 이메일을 통해 회사 사용자 검색
            company = User.objects.get(email=email, user_type="company")
            if company.check_password(password):
                return company
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None  # 동일한 이메일의 중복 데이터가 있는 경우
        return None
