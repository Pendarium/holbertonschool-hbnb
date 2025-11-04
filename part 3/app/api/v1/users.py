from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

users_ns = Namespace('users', description='User operations')


# models

user_model = users_ns.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'),
    'email': fields.String(
        required=True,
        description='Email of the user'),
    'password': fields.String(
        required=True,
        description='Password of the user'),
    'is_admin': fields.Boolean(
        required=False,
        description='Is the user admin?')
})


# test route proteger

@users_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Example of a protected route"""
        user_id = get_jwt_identity()
        claims = get_jwt()

        role = "admin" if claims.get('is_admin', False) else "user"

        return {
            'message': f'Hello {role} {user_id}',
            'is_admin': claims.get('is_admin', False)
        }, 200


# creation user list

@users_ns.route('/')
class UserList(Resource):
    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User successfully created')
    @users_ns.response(400, 'Email already registered')
    @jwt_required(optional=True)
    def post(self):
        """Register a new user (only admin can create another admin)"""
        user_data = users_ns.payload
        current_user_id = get_jwt_identity()

        # Vérifie si un utilisateur avec cet email existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Si on essaie de créer un admin
        if user_data.get("is_admin", False):
            # Si aucun utilisateur connecté → interdit
            if not current_user_id:
                return {'error':
                        'Authentication required to create an admin'}, 403

            # Vérifie si l’utilisateur actuel est admin
            current_user = facade.get_user(current_user_id)
            if not current_user or not current_user.is_admin:
                return {'error': 'Only admins can create another admin'}, 403

        # Création du nouvel utilisateur
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @users_ns.response(200, 'List of users retrieved successfully')
    @jwt_required()
    def get(self):
        """Retrieve a list of users (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_users()
        return [user.to_dict() for user in users], 200


# updt user

@users_ns.route('/<user_id>')
class UserResource(Resource):
    @users_ns.response(200, 'User details retrieved successfully')
    @users_ns.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID (self or admin only)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        if current_user != user_id and not claims.get("is_admin", False):
            return {'error': 'Access denied'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict(), 200

    @users_ns.expect(user_model)
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(404, 'User not found')
    @users_ns.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update user info
        (self or admin only, cannot change email/password)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        # Un utilisateur peut seulement modifier son propre profil (ou admin)
        if current_user != user_id and not claims.get("is_admin", False):
            return {'error': 'Unauthorized action'}, 403

        user_data = users_ns.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # modification du mot de passe
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


# promotion admin

@users_ns.route('/make-admin/<user_id>')
class MakeAdmin(Resource):
    @jwt_required()
    def post(self, user_id):
        """Promote a user to admin (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            facade.update_user(user_id, {"is_admin": True})
            return {'message':
                    f'User {user_id} promoted to admin successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
