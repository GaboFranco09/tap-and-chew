import os
from functools import wraps
from flask import request, jsonify


def internal_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        secret = request.headers.get('X-Internal-Secret')
        if not secret or secret != os.getenv('INTERNAL_SECRET'):
            return jsonify({
                'message': 'Acceso denegado. Debe pasar por el API Gateway.'
            }), 403
        return f(*args, **kwargs)
    return decorated