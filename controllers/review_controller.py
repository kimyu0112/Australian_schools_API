from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema

# reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:school_id>/reviews")
