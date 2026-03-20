from rest_framework.permissions import BasePermission  # Importa BasePermission desde `rest_framework.permissions`.







class IsAdminRole(BasePermission):  # Define la clase `IsAdminRole`.



    def has_permission(self, request, view):  # Define la funcion `has_permission`.



        return (  # Devuelve un valor (`return`).



            request.user  # Referencia `request.user` en la estructura/expresion.



            and request.user.is_authenticated  # Continua la expresion con `and`.



            and request.user.groups.filter(name="ADMIN").exists()  # Continua la expresion con `and`.



        )  # Cierra el bloque/estructura.







class IsClienteRole(BasePermission):  # Define la clase `IsClienteRole`.



    def has_permission(self, request, view):  # Define la funcion `has_permission`.



        return (  # Devuelve un valor (`return`).



            request.user  # Referencia `request.user` en la estructura/expresion.



            and request.user.is_authenticated  # Continua la expresion con `and`.



            and request.user.groups.filter(name="CLIENTE").exists()  # Continua la expresion con `and`.



        )  # Cierra el bloque/estructura.



