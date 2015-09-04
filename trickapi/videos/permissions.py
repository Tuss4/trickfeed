from rest_framework import permissions


class VideoViewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        can_post = not user.is_anonymous() and user.is_admin
        if request.method in permissions.SAFE_METHODS:
            return True
        return can_post
