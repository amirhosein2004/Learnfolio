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


class VideoPermission(BasePermission):
    """
    Custom permission for Video model:
    - Only admin can POST, PUT, PATCH, DELETE
    - For safe methods (GET, HEAD, OPTIONS):
        * If video is_free=True → everyone can access (even anonymous)
        * If video is not free:
            - Admin has access
            - Authenticated users who purchased the package (UserPackage exists)
            - Otherwise PermissionDenied
    """
    
    def has_permission(self, request, view):
        # For unsafe methods, only admin can perform them
        if request.method not in SAFE_METHODS:
            if not request.user.is_staff:
                raise PermissionDenied(detail=".شما به این بخش دسترسی ندارید")
            return request.user.is_authenticated
        
        # For safe methods, we need to check object-level permissions
        # Return True here and handle the logic in has_object_permission
        return True
    
    def has_object_permission(self, request, view, obj):
        # For unsafe methods, only admin can perform them
        if request.method not in SAFE_METHODS:
            if not request.user.is_staff:
                raise PermissionDenied(detail=".شما به این بخش دسترسی ندارید")
            return request.user.is_authenticated
        
        # For safe methods (GET, HEAD, OPTIONS)
        # If video is free, everyone can access
        if obj.is_free:
            return True
        
        # If video is not free, check additional conditions
        # Admin always has access
        if request.user.is_staff:
            return True
        
        # Check if user is authenticated and has purchased the package
        if request.user.is_authenticated:
            # Import here to avoid circular imports
            from education.models import UserPackage
            
            # Check if user has purchased this video's package
            if UserPackage.objects.filter(user=request.user, package=obj.package).exists():
                return True
        
        # If none of the above conditions are met, deny access
        raise PermissionDenied(detail=".برای دسترسی به این ویدیو باید پکیج مربوطه را خریداری کنید")
