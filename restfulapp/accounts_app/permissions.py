from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    According to https://www.django-rest-framework.org/api-guide/permissions/
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'author'):
            return obj.author == request.user

        return obj == request.user