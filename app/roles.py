from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from functools import wraps


class ROL:
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


def jwt_rol_required(roles):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):

            if current_user.rol not in roles:
                return jsonify({"status": "error", "message": "Permission denied. does not have the necessary permission"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
