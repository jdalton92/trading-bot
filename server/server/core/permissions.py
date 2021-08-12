from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission class to check that a user is the owner of a resource.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and (request.user.is_staff or obj.user == request.user):
            return True
        else:
            return PermissionDenied(
                {
                    "message": "You do not have correct permissions.",
                    "action": view.action,
                    "object_id": obj.id,
                }
            )
