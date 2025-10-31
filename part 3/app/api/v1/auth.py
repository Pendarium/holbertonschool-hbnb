from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash
from app.services import facade

# Namespace pour l'authentification
auth_ns = Namespace('auth', description='Authentication operations')

# Model pour login
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return JWT"""
        credentials = auth_ns.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not check_password_hash(user.password,
                                               credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        # is_admin true/false selon ton modèle
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200
