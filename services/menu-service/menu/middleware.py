import os
from rest_framework.permissions import BasePermission


class IsInternalRequest(BasePermission):
    """
    Permite acceso solo si la petición viene con el X-Internal-Secret correcto.
    Garantiza que todas las peticiones pasen por el API Gateway.
    """
    message = 'Acceso denegado. Debe pasar por el API Gateway.'

    def has_permission(self, request, view):
        secret = request.headers.get('X-Internal-Secret')
        return secret == os.getenv('INTERNAL_SECRET', '')