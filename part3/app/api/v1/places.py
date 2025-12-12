from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True, description='Latitude of the place'),
    'longitude': fields.Float(
        required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(
        fields.String, description='List of amenity IDs'),
    'reviews': fields.List(
        fields.String, description='List of review IDs')
    })


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Invalid id')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place"""
        # fetch token identity
        current_user = facade.get_token_identity()
        # fetch payload
        place_data = api.payload
        # check identity
        if current_user['id'] != place_data['owner_id'] and not current_user['role']:
            return {"error": "Unauthorized action"}, 403
        # create place / checks in facade
        try:
            place = facade.create_place(place_data)
        except LookupError as e:
            return {"error": str(e)}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        if not place:
            return {"error": "Invalid input data"}, 400
        # add the palce to the owner's place list
        owner = facade.get_user(place.owner_id)
        owner.add_place(place)
        return place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        place = facade.get_all_places()
        new_list = []
        for element in place:
            new_list.append(element.to_dict())
        return new_list, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": facade.get_user(place.owner_id).to_dict(),
            "amenities":
            [element.to_dict()
             for element in place.amenities],
            "reviews": [element.to_dict()
                        for element in place.reviews]
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized acion')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        current_user = facade.get_token_identity()
        datas = api.payload
        place = facade.get_place(place_id)  # return a place object
        if current_user['id'] != place.owner_id and not current_user['role']:
            return {
                "error": "Unauthorized action: you are not the place owner"
                }, 403
        if not place:
            return {"error": "Place not found"}, 404
        try:
            facade.update_place(place_id, datas)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        place_reviews_list = place.reviews
        return [review.to_dict() for review in place_reviews_list], 200
