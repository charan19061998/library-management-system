from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only active admins to edit data.
    Regular active users can read data.
    Inactive users are denied all access.
    """

    def has_permission(self, request, view):
        # Deny access to inactive users
        if not request.user.is_active:
            return False

        # Allow admin users full access
        if request.user.is_staff:
            return True

        # Allow read-only access to non-admin active users
        return request.method in ['GET', 'HEAD', 'OPTIONS']
