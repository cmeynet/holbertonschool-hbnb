from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def admin_required(fn):
    """
    Authorizes only JWT requests with is_admin=True
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # * : args without name & ** args with name
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return jsonify({"error": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper
