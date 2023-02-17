from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHeHim(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
