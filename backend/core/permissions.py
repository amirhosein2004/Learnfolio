from rest_framework.permissions import BasePermission, SAFE_METHODS
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


class UserAdminIsAuthenticated(UserIsAuthenticated):
    """Allow only admin users and authenticated users."""

    def has_permission(self, request, view):
        if not request.user.is_staff:
            raise PermissionDenied(detail=".شما به این بخش دسترسی ندارید")
        return super().has_permission(request, view)


class UserAdminOrReadOnly(BasePermission):
    """
    everyone read-only (GET, HEAD, OPTIONS) 
    only admin can POST, PUT, PATCH, DELETE
    """

    def has_permission(self, request, view):
        # methods read-only free for evryone
        if request.method in SAFE_METHODS:
            return True

        # for change methods only admin can
        if not request.user.is_staff:
            raise PermissionDenied(detail=".شما به این بخش دسترسی ندارید")

        # if admin check ia authenticated
        return request.user.is_authenticated
