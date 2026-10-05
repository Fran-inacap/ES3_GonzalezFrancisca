# NutriPet/permissions.py
from rest_framework import permissions


class SoloStaffBorra(permissions.BasePermission):
    """
    Permite todas las operaciones a usuarios autenticados,
    pero restringe el borrado (DELETE) únicamente a usuarios staff.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)
