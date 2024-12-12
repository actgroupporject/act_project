import re
from typing import Any

import requests  # type: ignore
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError  # type: ignore
from decouple import config
from typing import Any
import requests
from django.core.exceptions import ValidationError

class PasswordValidator:
    def __call__(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError(e)

    def validate(self, password, user=None):
        # 비밃번호 유효성검사
        if len(password) < 8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다")
        if not re.search("[a-zA-Z]", password):
            raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다")
        if not re.search("[0-9]", password):
            raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다")
        if not re.search("[!@#$%^&*()]", password):
            raise ValidationError("비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다")

    def get_help_text(self):
        return "비밀번호는 8자리 이상이며 영문, 숫자, 특수문자(!@#$%^&*())를 포합해야 합니다"





def validate_kakao_address(value: Any) -> None:
    """
    카카오 API를 사용하여 주소 유효성을 검증하는 함수.
    유효하지 않은 경우 ValidationError를 발생시킵니다.

    :param value: 검증할 주소 값
    """
    API_KEY = config("KAKAO_CLIENT_ID")
    url = f"https://dapi.kakao.com/v2/local/search/address.json?query={value}"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}

    try:
        # API 요청
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValidationError(f"카카오 API 요청 실패: 상태 코드 {response.status_code}")

        # JSON 데이터 파싱 및 결과 확인
        data = response.json()
        if not data.get("documents"):
            raise ValidationError("유효한 주소 결과를 찾을 수 없습니다.")
    except requests.RequestException as e:
        # 요청 예외 처리
        raise ValidationError(f"카카오 API 요청 중 오류 발생: {e}")
