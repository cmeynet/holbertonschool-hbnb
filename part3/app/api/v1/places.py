from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("places", description="Place operations")

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

place_create_model = api.model(
    "PlaceCreate",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude"),
        "longitude": fields.Float(required=True, description="Longitude"),
        "amenities": fields.List(
            fields.String, required=True, description="List of amenity IDs"
        ),
    },
)

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


@api.route("/")
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Bad request")
    @api.response(404, "User or amenity not found")
    def post(self):
        """
        Create a new place — authenticated user becomes owner
        """
        current_user_id = get_jwt_identity()
        payload = api.payload

        try:
            place = facade.create_place(current_user_id, payload)
            return place.to_dict(), 201
        except PermissionError as error:
            return {"error": str(error)}, 403
        except KeyError as error:
            return {"error": str(error)}, 404
        except ValueError as error:
            return {"error": str(error)}, 400

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Public: list all places"""
        places = facade.get_all_places()
        return [{"id": p.id, "title": p.title, "price": p.price} for p in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Public: get a single place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": { "id": place.owner.id }
            }, 200


    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(403, "Unauthorized action") # the only code required by the instructions
    @api.response(400, "Bad request")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """
        Owner or admin: update a place
        """
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False) 
        payload = api.payload

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and str(place.owner.id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403
        try:
            updated = facade.update_place(current_user_id, place_id, payload)
            return updated.to_dict(), 200
        except ValueError as err:
            return {"error": str(err)}, 400

@api.route("/<place_id>/amenities")
class PlaceAmenities(Resource):
    amenity_ids_model = api.model(
        "AmenityIDList",
        {
            "amenities": fields.List(
                fields.String, required=True, description="List of amenity IDs"
            )
        },
    )

    @jwt_required()
    @api.expect(amenity_ids_model, validate=True)
    @api.response(200, "Amenities added successfully")
    @api.response(400, "Bad request")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place or amenity not found")
    def post(self, place_id):
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)
        amenity_ids = api.payload.get("amenities", [])
        try:
            place = facade.get_place(place_id)
            if not place:
                raise KeyError("Place not found")
            if not is_admin and str(place.owner.id) != str(current_user_id):
                return {"error": "Unauthorized action"}, 403

            for aid in amenity_ids:
                amenity = facade.get_amenity(aid)
                if not amenity:
                    raise KeyError(f"Amenity not found: {aid}")
                place.add_amenity(amenity)
            return {"message": "Amenities added successfully"}, 200
        except KeyError as error:
            return {"error": str(error)}, 404
        except ValueError as error:
            return {"error": str(error)}, 400


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.response(200, "Reviews retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in place.reviews], 200
