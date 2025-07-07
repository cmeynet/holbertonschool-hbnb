from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# # Define the models for amenities, users & places

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

place_create_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    # “owner.id” is deliberately excluded from the input template
    # The authenticated user ID (from JWT) is injected server-side to prevent spoofing
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(description="Price per night"),
        "latitude": fields.Float(description="Latitude"),
        "longitude": fields.Float(description="Longitude"),
        "amenities": fields.List(
            fields.String, description="List of amenity IDs"
        ),
    },
)



@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place (authenticated)"""
        current_user = get_jwt_identity()
        place_data = api.payload

        try:
            new_place = facade.create_place({**place_data, 'owner_id': current_user})
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_list(), 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (owner only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if str(place.owner.id) != str(current_user):
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_place(place_id, api.payload)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @jwt_required()
    @api.expect(api.model('AmenityIDList', {
        'amenities': fields.List(fields.String, required=True,
                                 description="List of amenity IDs")
    }), validate=True)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        amenity_ids = api.payload["amenities"]
        if not amenity_ids:
            return {'error': 'Invalid input data'}, 400

        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if str(place.owner.id) != str(current_user):
            return {'error': 'Unauthorized action'}, 403

        for amenity_id in amenity_ids:
            if not facade.get_amenity(amenity_id):
                return {'error': f'Invalid amenity ID: {amenity_id}'}, 400
            place.add_amenity(amenity_id)
        return {'message': 'Amenities added successfully'}, 200


@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
