from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class UserIsNotAuthenticated(BasePermission):
    """only Anonymous users can(no login)"""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            raise PermissionDenied(detail=".شما قبلاً وارد شده‌اید")
        return True
    
class UserIsAuthenticated(BasePermission):
    """only Authenticated users can(login)"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail=".ابتدا وارد شوید")
        return True

class HasNoPassword(BasePermission):
    """Allow only users who haven't set a password yet."""

    def has_permission(self, request, view):
        if request.user.has_usable_password():
            raise PermissionDenied(detail=".شما قبلا رمز عبور خود را تنظیم کرده اید مجوز این کار را ندارید") 
        return True

class HasPassword(BasePermission):
    """Allow only users who have already set a password."""

    def has_permission(self, request, view):
        if not request.user.has_usable_password():
            raise PermissionDenied(detail=".ابتدا برای خود رمز عبور را تنظیم کنید")
        return True