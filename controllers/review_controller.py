from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.school import School

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:school_id>/reviews")

@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(school_id):
    body_data = request.get_json()
    
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:
        review = Review(
            review_title=body_data.get("review_title"),
            review_content=body_data.get("review_content"),
            user_id=get_jwt_identity(),
            school=school
        )
    
        db.session.add(review)
        db.session.commit()

        return review_schema.dump(review), 201

    else:
        return {"error": f"School with id {school_id} not found."}, 404


