from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsNotAuthenticated(BasePermission):
    """
    only Anonymous users can(no login)
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            raise PermissionDenied(detail=".شما قبلاً وارد شده‌اید")
        return True