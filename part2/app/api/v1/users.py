from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Définition du modèle pour Swagger et validation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        if not user_data or not isinstance(user_data, dict):
            return {"error": "Invalid JSON"}, 400

        # Vérifier l'email déjà utilisé
        existing_user = facade.get_user_by_email(user_data.get('email', ''))
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Créer l'utilisateur et capturer les erreurs de validation (email)
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Return all users"""
        all_users = facade.get_all()
        return [user.to_dict() for user in all_users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        data = api.payload
        if not data or not isinstance(data, dict):
            return {"error": "Invalid JSON"}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Appel à la façade avec gestion des erreurs de validation
        try:
            updated_user = facade.update_user(user_id, data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
