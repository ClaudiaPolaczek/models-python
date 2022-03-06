from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if int(request.resolver_match.kwargs.get('pk')) == request.user.id:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False