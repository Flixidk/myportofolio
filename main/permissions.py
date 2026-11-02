from rest_framework.permissions import BasePermission, SAFE_METHODS


EDITOR_GROUP_NAME = "Editors"


def user_is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP_NAME).exists()


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can make changes."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and user_is_editor(request.user)
        )
