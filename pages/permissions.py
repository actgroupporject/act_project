from rest_framework import permissions

"""
IsOwnerOrReadOnly, IsCompanyUser
객체 소유자나 회사 사용자만 특정 작업을 수행할 수 있도록 제한
"""


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_company
