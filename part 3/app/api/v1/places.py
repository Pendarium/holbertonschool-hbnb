from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# models
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

# model
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place (authenticated users only)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (public)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_list(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (only by owner)"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Vérifier que l'utilisateur est bien le propriétaire
        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        amenities_ids = place_data.pop('amenities', None)
        # retirer amenities du dict

        try:
            # Mettre à jour les autres champs via la façade
            updated_place = facade.update_place(place_id, place_data)

            # Gérer les amenities si fournis
            if amenities_ids:
                updated_place.amenities.clear()  # vider l'ancienne liste
                for a_id in amenities_ids:
                    amenity = facade.get_amenity(a_id)
                    if not amenity:
                        return {'error': f'Amenity {a_id} not found'}, 400
                    updated_place.add_amenity(amenity)

            return {
                'message': 'Place updated successfully',
                'place': updated_place.to_dict_list()
            }, 200

        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(api.model('AmenitiesList', {
        'amenities': fields.List(fields.String, required=True,
                                 description="List of amenity IDs")
    }))
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self, place_id):
        """Add amenities to a place (only owner)"""
        current_user_id = get_jwt_identity()
        payload = api.payload
        amenity_ids = payload.get('amenities', [])

        if not amenity_ids:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        for amenity_id in amenity_ids:
            a = facade.get_amenity(amenity_id)
            if not a:
                return {'error': f'Amenity {amenity_id} not found'}, 400
            place.add_amenity(a)

        return {'message': 'Amenities added successfully'}, 200


@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
