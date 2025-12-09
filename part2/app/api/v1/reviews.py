from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'comment': fields.String(
        required=True, description='Comment of the review'),
    'user_id': fields.String(
        required=True, description='ID of the user writing the review'),
    'place_id': fields.String(
        required=True, description='ID of the place being reviewed'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the review (1 to 5)',
        min=1,
        max=5
    )
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

    def delete(self, review_id):
        """Supprime une review par son ID"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted", "id": review_id}, 200
