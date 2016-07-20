# -*- coding: utf-8 -*- 
from rest_framework import permissions

    
class IsOwnerOrEditor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        
        # All permissions are allowed to editors
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Editor' in user_groups:
            return True

        # Otherwise permissions are only allowed to the owner of the object
        if hasattr(obj, 'username'):
            return obj == request.user and request.user.is_authenticated()
        else:
            return obj.owner == request.user and request.user.is_authenticated()




class IsEditor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        # All permissions are allowed to editors
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Editor' in user_groups:
            return True

        return False


    def has_object_permission(self, request, view, obj):
        # All permissions are allowed to editors
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Editor' in user_groups:
            return True

        return False
