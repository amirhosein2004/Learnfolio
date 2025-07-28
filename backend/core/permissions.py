from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
    only Anonymous users can(no login)
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated