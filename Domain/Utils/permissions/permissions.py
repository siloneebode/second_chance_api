from rest_framework import permissions

from Domain.phone.models import Phone


# permission qui vérifie si le user n'est pas banni.
class CanDoSomething(permissions.BasePermission):
    message = "Erreur, ce compte est bloqué"

    def has_permission(self, request, view):
        return request.user.banned_at is None


# cette permission vérifie si personne n'a bloqué l'autre avant de follow
class UserNotBlocked(permissions.BasePermission):

    def has_permission(self, request, view):
        pass


# cette permission vérifie si l'user est déja abonné pour le désabonner.
class HasAlreadyFollow(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# cette permission vérifie si l'utilisateur a le droit de se connecter
class LoginPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pass


class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user is None


class CanManageOffer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user or obj.product.owner == request.user


class CanActivateWallet(permissions.BasePermission):

    def has_permission(self, request, view):
        if Phone.objects.filter(is_verified=True, owner=request.user).exists():
            return True
        return False


class CanCreateOrder(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.email_confirmed:
            return True


class CanManageOrder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.product.owner == request.user
