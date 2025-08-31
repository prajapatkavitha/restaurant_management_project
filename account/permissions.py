# account/permissions.py

from rest_framework import permissions
from .models import User

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == User.Role.ADMIN

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow manager or admin users access.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == User.Role.MANAGER or request.user.role == User.Role.ADMIN)

class IsWaiter(permissions.BasePermission):
    """
    Custom permission to only allow waiter users access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == User.Role.WAITER

class IsCashier(permissions.BasePermission):
    """
    Custom permission to only allow cashier users access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == User.Role.CASHIER
