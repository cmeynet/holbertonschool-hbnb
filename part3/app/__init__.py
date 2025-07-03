from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.extensions import bcrypt

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Flask application factory that instantiates the app with a configuration class
    """
    # Étape n°1 : Charger la configuration de l'application avant d'initialiser les extensions(BD...)
    app = Flask(__name__)
    app.config.from_object(config_class)
    

    # Étape n°2 : Initialiser Bcrypt avec l’application Flask
    bcrypt.init_app(app)
    jwt.init_app(app) 

    # Étape n°3 :   Créer l'API Flask-RESTx
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API"
    )

    # Étape n°4 : Enregistrer les namespaces pour activer les routes de chaque fonctionnalité (users, places, reviews, etc.) 

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app
