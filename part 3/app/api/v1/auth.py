from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token
# from app.extensions import bcrypt

api = Namespace('auth', description='User operations')

user_authentification = api.model('auth', {
    'email': fields.String(
        required=True, description='Email of the user'),
    'password': fields.String(
        required=True, description='Password of the user')
})


@api.route('/login')
class Userlogin(Resource):
    @api.expect(user_authentification)
    @api.response(401, "Invalid credentials")
    @api.response(200, "token")
    def post(self):
        user_data = api.payload
        user_data_email = user_data['email']
        existing_user = facade.get_user_by_email(user_data_email)
        if not existing_user:
            return {"error": "Invalid credentials"}, 401
        if existing_user.verify_password(user_data['password']):
            access_token = create_access_token(
                identity=str(existing_user.id),
                additional_claims={"is_admin": existing_user.is_admin}
                # extra info here
            )

            return {'access_token': access_token}, 200
        else:
            return {"error": "Invalid credentials"}, 401
