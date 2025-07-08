from flask_restx import Namespace, Resource, fields
from app.extensions import admin_required
from app.services import facade

api = Namespace("admin_amenities", description="Admin: manage amenities")

amenity_in = api.model("AdminAmenityIn", {
    "name": fields.String(required=True, description="Amenity name")
})
amenity_out = api.clone("AdminAmenityOut", amenity_in, {
    "id": fields.String
})

@api.route("/")
class AdminAmenityList(Resource):
    @admin_required
    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out, code=201)
    def post(self):
        """
        Add a new amenity (admin only not all users)
        """
        data = api.payload
        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201


@api.route("/<amenity_id>")
class AdminAmenityResource(Resource):
    @admin_required
    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out)
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """
        Modify an amenity (admin only not all users!!)"""
        if not facade.get_amenity(amenity_id):
            return {"error": "Amenity not found"}, 404

        updated = facade.update_amenity(amenity_id, api.payload)
        return updated.to_dict()
