import re  # type: ignore

from django import forms  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore

from .models import Company, User  # type: ignore

# def validate_kakao_address(value):
#     API_KEY = 'ba45edb9c912322af612bf80a2376df7'
#     url = f"https://dapi.kakao.com/v2/local/search/address.json?query={value}"
#     headers = {"Authorization": f"KakaoAK {API_KEY}"}
#     response = requests.get(url, headers=headers).json()
#
#     if response.status_code != 200:
#         raise ValidationError("카카오 API 요청 실패: 상태 코드 {}".format(response.status_code))
#     data = response.json()
#     if 'documents' in data:
#         return data['documents']  # 검색 결과 리스트 반환
#     else:
#         raise ValidationError("유효한 주소 결과를 찾을 수 없습니다.")


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            raise ValidationError("비밀번호는 영문자와 숫자를 포함해야 합니다.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "비밀번호가 일치하지 않습니다.")


class CompanyRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = Company
        fields = ["email", "name", "password", "phone_number", "company_url"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Company.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            raise ValidationError("비밀번호는 영문자와 숫자를 포함해야 합니다.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "비밀번호가 일치하지 않습니다.")
