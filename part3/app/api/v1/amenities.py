from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Ressource already exist')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity"""
        # fetch identity token
        current_user = facade.get_token_identity()
        # check role
        if not current_user['role']:
            return {"error": "Admin privileges required"}, 403
        data = api.payload
        existing_amenity = facade.get_by_attribute("name", data['name'])
        if existing_amenity:
            return {"error": "amenity already exist"}, 409
        amenity = facade.create_amenity(data)
        if not amenity:
            return {"error": "Invalid input data"}, 400
        return amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        new_list = []
        for element in amenities:
            new_list.append(element.to_dict())
        return new_list


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict()

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Name already exist')
    def put(self, amenity_id):  # paramètre de la route
        """Update an amenity's information"""
        # fetch identity token
        current_user = facade.get_token_identity()
        # check role
        if not current_user['role']:
            return {"error": "Admin privileges required"}, 403
        data = api.payload
        if "name" not in data or data["name"] == "":
            return {"error": "Invalid input data"}, 400
        existing_amenity = facade.get_by_attribute("name", data['name'])
        if existing_amenity:
            return {"error": "amenity already exist"}, 409
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        facade.update_amenity(amenity_id, data)
        return {"message": "Amenity updated successfully"}, 200
