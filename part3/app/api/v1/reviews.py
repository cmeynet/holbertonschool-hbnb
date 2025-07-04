from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('reviews', description='Review operations')

# Revision model defined for data validation and documentation

review_in_model = api.model('ReviewIn', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)', min=1, max=5
    ),
    # "user_id" is deliberately excluded because it is injected from JWT
    'place_id': fields.String(required=True, description='ID of the place')
})

review_out_model = api.inherit('ReviewOut', review_in_model, {
    'id': fields.String(readonly=True, description='Review ID'),
    'user_id': fields.String(readonly=True, description='Author ID')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_in_model, validate=True)
    @api.marshal_with(review_out_model, code=201)
    @api.response(400, 'Invalid input data or business rule violated')
    def post(self):
        """
        Register a new review
        """
        current_user = get_jwt_identity()
        data = request.get_json()

        # If place must exist
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        # Impossible to value your own home
        if place.owner_id == current_user:
            return {'error': 'User cannot review their own place'}, 400

        # Not possible to post a review twice on the same property
        if facade.user_already_reviewed(current_user, place.id):
            return {'error': 'You have already reviewed this place'}, 400

        # Create review
        review = facade.create_review({
            **data,
            'user_id': current_user
        })
        return review.to_dict(), 201

    @api.marshal_list_with(review_out_model)
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Public: list all reviews
        """
        return [r.to_dict() for r in facade.get_all_reviews()], 200

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
