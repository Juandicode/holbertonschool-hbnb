from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade as hbnb_facade

api = Namespace('reviews', description='Review operations')

# Models
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.marshal_with(review_response_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        try:
            data = request.get_json()
            review = hbnb_facade.create_review(data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(404, str(e))

    @api.marshal_list_with(review_response_model)
    def get(self):
        """Get all reviews"""
        return hbnb_facade.get_all_reviews()

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details"""
        review = hbnb_facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review

    @api.expect(review_model)
    @api.response(200, 'Review updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        try:
            data = request.get_json()
            review = hbnb_facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(404, str(e))

    @api.response(200, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            hbnb_facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get reviews for a place"""
        try:
            return hbnb_facade.get_reviews_by_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))
