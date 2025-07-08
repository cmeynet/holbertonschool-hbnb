from flask_restx import Namespace, Resource, fields
from app.extensions import admin_required
from app.services import facade

api = Namespace("admin_users", description="Admin: manage any user")

user_in = api.model("AdminUserIn", {
    "email":      fields.String(required=True),
    "password":   fields.String(required=True),
    "first_name": fields.String,
    "last_name":  fields.String,
    "is_admin":   fields.Boolean(default=False)
})

user_out = api.clone("AdminUserOut", user_in, {
    "id": fields.String
})


@api.route("/")
class AdminUserList(Resource):
    @admin_required
    @api.expect(user_in, validate=True)
    @api.marshal_with(user_out, code=201)
    @api.response(409, "Email already registered")
    def post(self):
        """
        Create a new user (admin only)
        """
        data = api.payload
        if facade.get_user_by_email(data["email"]):
            return {"error": "Email already registered"}, 409

        user = facade.create_user(data)
        return user.to_dict(), 201


@api.route("/<user_id>")
class AdminUserResource(Resource):
    @admin_required
    @api.expect(user_in, validate=True)
    @api.marshal_with(user_out)
    @api.response(404, "User not found")
    @api.response(409, "Email already in use")
    def put(self, user_id):
        """
        Modify any user (admin only)
        """
        payload = api.payload or {}

        if "email" in payload:
            other = facade.get_user_by_email(payload["email"])
            if other and str(other.id) != str(user_id):
                return {"error": "Email already in use"}, 409

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        updated = facade.update_user(user_id, payload)
        return updated.to_dict()
