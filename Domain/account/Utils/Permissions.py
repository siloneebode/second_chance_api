from rest_framework import permissions

from rest_framework import permissions
from Domain.additionalInfo.models import IpBlocked


class BlockListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ip = request.META['REMOTE_ADDR']
        blocked = IpBlocked.objects.filter(ip=ip).exists()
        return not blocked


class IsOwnerRessourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
