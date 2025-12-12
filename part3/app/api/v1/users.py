from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from jwt import ExpiredSignatureError

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True, description='First name of the user'),
    'last_name': fields.String(
        required=True, description='Last name of the user'),
    'email': fields.String(
        required=True, description='Email of the user'),
    'password': fields.String(
        required=True, description='Password of the user')
})


@api.route('/')
class UserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new user"""
        # initialize role variable to false
        role = False
        # verify if there is a token and validate it if so
        try:
            verify_jwt_in_request(optional=True)
            current_user = facade.get_token_identity()
        # le bloc except va ignorer un token expiré rendant possible
        # de créer un nouveau user non admin par quelqu'un
        # ayant un token invalid, comme s'il était non logué
        except (JWTExtendedException,
                ExpiredSignatureError,
                NoAuthorizationError):
            current_user = None
        # fetch current user from token
        if current_user:
            role = current_user['role']
        # fetch datas from payload
        user_data = api.payload
        # check if tries to create an admin
        if 'is_admin' in user_data:
            if user_data['is_admin'] and not role:
                return {"error": "Unauthorized action"}, 403
        if "@" not in user_data['email']:
            return {"error": "Invalid input data: @ char is missing"}, 400
        if user_data['first_name'] == "":
            return {"error": "Invalid input data: empty string"}, 400
        if user_data['last_name'] == "":
            return {"error": "Invalid input data: empty string"}, 400
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
            }, 201

    @jwt_required()
    @api.response(200, 'OK')
    @api.response(403, "Admin privileges required")
    def get(self):
        """
        This function responsible for
        fetching all users informations
        """
        current_user = facade.get_token_identity()
        if not current_user['role']:
            return {"error": "Admin privileges required"}, 403
        users = facade.get_all()
        new_list = []
        for element in users:
            new_list.append(element.to_dict())
        return new_list


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """This function retrieve of user
        by its id
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            # 'places': user.places
            }, 200

    @jwt_required()
    @api.response(200, "OK")
    @api.response(404, "Not Found")
    @api.response(400, 'Bad Request')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """
        This method in charge of modifying user's
        informations
        """
        # fetch token identity
        current_user = facade.get_token_identity()
        # fetch payload
        update_datas = api.payload
        # check authorization :
        if current_user['id'] != user_id and not current_user['role']:
            return {"error": "Unauthorized action"}, 403
        # mai and password authorization
        if ('email' in update_datas or 'password' in update_datas) and not current_user['role']:
            return {'error': 'You cannot modify email or password.'}, 400
        # rebuild the user
        user = facade.get_user(user_id)
        if not user:
            return {"error": "Not found"}, 404
        # check if is trying to update with an existing email
        if 'email' in update_datas:
            user_mail = facade.get_user_by_email(update_datas['email'])
            if user_mail and user_mail.id != user_id:
                return {"error": "Email already exist"}, 400
            if "@" not in update_datas['email']:
                return {"error": "Invalid data input"}, 400
        # update
        facade.update(user_id, update_datas)
        return user.to_dict()
