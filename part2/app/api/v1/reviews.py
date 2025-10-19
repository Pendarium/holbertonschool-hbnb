from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Input model for creating/updating reviews
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True,
                             description='ID of the user writing the review'),
    'place_id': fields.String(required=True,
                              description='ID of the place being reviewed')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Invalid JSON"}, 400
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Internal server error"}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Invalid JSON"}, 400
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Internal server error"}, 500
