from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.extensions import bcrypt

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns

jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Flask application factory that instantiates the app with a configuration class
    """
    # Step 1: Load application configuration before initializing extensions(BD...)
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Step 2: Initialize Bcrypt with the Flask application
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Step 3: Create the Flask-RESTx API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API"
    )

    # Step 4: Register namespaces to activate routes for each feature (users, places, reviews, etc.)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(protected_ns, path='/api/v1')
    api.add_namespace(auth_ns, path="/api/v1/auth")
    return app
