from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Company, User


# 유저 회원가입 뷰
def user_register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        # 주소, 생년월일, 전화번호
        if password != confirm_password:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect("user_register")

        try:
            User.objects.create_user(email=email, name=name, password=password)
            messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect("user_login")
        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {e}")
            return redirect("user_register")
    return render(request, "user_register.html")


# 회사 회원가입 뷰
def company_register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone_number = request.POST.get("phone_number")
        company_url = request.POST.get("company_url")
        # 담당자 명, 사업자 등록번호
        if password != confirm_password:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect("company_register")

        try:
            Company.objects.create_user(
                email=email, name=name, password=password, phone_number=phone_number, company_url=company_url
            )
            messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect("company_login")
        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {e}")
            return redirect("company_register")
    return render(request, "company_register.html")


# 로그인 뷰 (유저와 회사 공통)
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")  # 'user' 또는 'company'

        # 인증 시도
        user = authenticate(request, email=email, password=password)
        if user:
            if user_type == "user" and isinstance(user, User):
                login(request, user)
                messages.success(request, f"{user.name}님, 환영합니다!")
                return redirect("user_home")
            elif user_type == "company" and isinstance(user, Company):
                login(request, user)
                messages.success(request, f"{user.name}님, 환영합니다!")
                return redirect("company_home")
            else:
                messages.error(request, "잘못된 사용자 유형입니다.")
        else:
            messages.error(request, "이메일 또는 비밀번호가 올바르지 않습니다.")
    return render(request, "login.html")


# 로그아웃 뷰
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("login")
