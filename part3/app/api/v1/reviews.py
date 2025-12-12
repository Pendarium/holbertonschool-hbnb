from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'ID not found')
    def post(self):
        """Register a new review"""
        # fetch token identity
        current_user = facade.get_token_identity()
        # fetch payload
        datas = api.payload
        user_full = facade.get_user(current_user['id'])
        # check the user is the owner of the place
        for place in user_full.places:
            if datas["place_id"] == place.id:
                return {"error": "You cannot review your own place."}, 400
        # check if author already reviewed the place
        for review in user_full.reviews:
            review = facade.get_review(review.id)
            if datas["place_id"] == review.place_id:
                return {"error": "You have already reviewed this place."}, 400
        try:
            review = facade.create_review(datas)
        except ValueError as e:
            return {"error": str(e)}, 400
        except LookupError as e:
            return {"error": str(e)}, 404
        if not review:
            return {"error": "Invalid input data"}, 400
        # add the review to the author:
        # user_full.add_review(review.id)
        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews_list = facade.get_all_reviews()
        new_list = []
        for element in all_reviews_list:
            new_list.append({"id": element.id,
                             "comment": element.comment,
                             "rating": element.rating})
        return new_list, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict()

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        # fetch token identity
        current_user = facade.get_token_identity()
        # fetch payload
        datas = api.payload
        # call the review
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        # check author :
        if not current_user['id'] == review.user_id:
            return {
                "error": "Unauthorized action: "
                "you have not authored this review"}, 403
        # update :
        try:
            facade.update_review(review_id, datas)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        # fetch token identity
        current_user = facade.get_token_identity()
        # call the review
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        # check author :
        if not current_user['id'] == review.user_id and not current_user['role']:
            return {
                "error": "Unauthorized action: "
                "you have not authored this review"}, 403
        # delete the review:
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
