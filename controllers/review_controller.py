from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.school import School

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:school_id>/reviews")

@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(school_id):
    body_data = review_schema.load(request.get_json(), partial=True)
    
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


@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(school_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    if review:
        db.session.delete(review)
        db.session.commit()
        return {"message": f"Review '{review.review_title}' deleted successfully"}
    
    else:
        return {"error": f"Review with id {review_id} not found"}, 404

@reviews_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_review(school_id, review_id):
    body_data = review_schema.load(request.get_json())

    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    if review:
        review.review_title = body_data.get("review_title") or review.review_title
        review.review_content = body_data.get("review_content") or review.review_content
    
        db.session.commit()
      
        return review_schema.dump(review)

    else:
        return {"error": f"Revuew with id {review_id} not found"}, 404