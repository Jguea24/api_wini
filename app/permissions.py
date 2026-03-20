from rest_framework.permissions import BasePermission  # comentario

class IsAdminRole(BasePermission):  # comentario
    def has_permission(self, request, view):  # comentario
        return (  # comentario
            request.user  # comentario
            and request.user.is_authenticated  # comentario
            and request.user.groups.filter(name="ADMIN").exists()  # comentario
        )  # comentario

class IsClienteRole(BasePermission):  # comentario
    def has_permission(self, request, view):  # comentario
        return (  # comentario
            request.user  # comentario
            and request.user.is_authenticated  # comentario
            and request.user.groups.filter(name="CLIENTE").exists()  # comentario
        )  # comentario
