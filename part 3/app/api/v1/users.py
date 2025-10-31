from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

users_ns = Namespace('users', description='User operations')


# MODELS

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

# ROUTE PROTÉGÉE TEST


@users_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Example of a protected route"""
        user_id = get_jwt_identity()   # récupère l'ID de l'utilisateur
        claims = get_jwt()             # récupère les claims du JWT (is_admin)

        role = "admin" if claims.get('is_admin', False) else "user"

        return {
            'message': f'Hello {role} {user_id}',
            'is_admin': claims.get('is_admin', False)
        }, 200


# CRÉATION ET LISTE USERS

@users_ns.route('/')
class UserList(Resource):
    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User successfully created')
    @users_ns.response(400, 'Email already registered')
    def post(self):
        """Register a new user (anyone can create admin for testing)"""
        user_data = users_ns.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

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


# USER DETAIL / UPDATE

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
        """Update user info (self or admin only)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        if current_user != user_id and not claims.get("is_admin", False):
            return {'error': 'Access denied'}, 403

        user_data = users_ns.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


# PROMOTE USER TO ADMIN

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
            user.is_admin = True
            facade.update_user(user_id, {"is_admin": True})
            return {'message': f'User {
                user_id} promoted to admin successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
