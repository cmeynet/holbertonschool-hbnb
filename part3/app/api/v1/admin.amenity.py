from flask_restx import Namespace, Resource, fields
from app.extensions import admin_required
from app.services import facade
