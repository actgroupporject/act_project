from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.http import HttpRequest
from rest_framework.request import Request


class CustomOAuth2Provider(OAuth2Provider):
    def get_scope(self, request: HttpRequest = None):  # type: ignore
        if request and isinstance(request, Request):
            data = request.data
        else:
            data = {}
        extra_scope = data.get("extra_scope", "")
        base_scope = ["email", "profile"]
        return base_scope + [extra_scope] if extra_scope else base_scope
