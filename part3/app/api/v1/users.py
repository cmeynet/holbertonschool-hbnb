from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description="Password of the user")
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created with success')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Input data invalid')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Vérifie si l’e-mail est déjà utilisé
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 409

        try:
            # Crée un nouvel utilisateur, le mot de passe est haché automatiquement
            new_user = facade.create_user(user_data)

            # Réponse simple : pas de mot de passe
            return {'id': str(new_user.id), 'message': 'User created'}, 201

        except Exception as error:
            return {'error': str(error)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Get all users (without passwords).
        """
        users = facade.get_users()
        return [user.to_dict() for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve one user (no password returned)."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'You cannot modify email or password.')  # 1st code required by the instructions
    @api.response(403, 'Unauthorized action') # 2nd code required by the instructions
    def put(self, user_id):
        current_user = get_jwt_identity()
        if str(current_user) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        payload = api.payload or {}

        if 'email' in payload or 'password' in payload:
            return {'error': 'You cannot modify email or password'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        updated = facade.update_user(current_user, user_id, payload)
        return updated.to_dict(), 200
    