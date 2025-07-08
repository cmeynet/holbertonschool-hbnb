from flask_bcrypt import Bcrypt
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
bcrypt = Bcrypt()
