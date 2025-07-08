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
