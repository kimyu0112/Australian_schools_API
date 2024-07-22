from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.user import User, user_schema, users_schema
from models.school import School
from utils import authorise_as_admin

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:school_id>")

@reviews_bp.route("/<int:user_id>/reviews")
@jwt_required()
def retrieve_review_by_userid(user_id):
    stmt_user = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt_user)

    if user:
        stmt_reviews = db.select(Review).filter_by(user_id=user_id)
        reviews = db.session.scalars(stmt_reviews)
        return reviews_schema.dump(reviews), 200
    
    else:
        return {"error": f"User with id {user_id} not found."}, 404


@reviews_bp.route("/reviews")
def retrieve_review_by_school(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_reviews = db.select(Review).filter_by(school_id=school_id)
        reviews = db.session.scalars(stmt_reviews)
        return reviews_schema.dump(reviews), 200

    else:
        return {"error": f"School with id {school_id} not found."}, 404


@reviews_bp.route("/reviews", methods=["POST"])
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


@reviews_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(school_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    if review:
        is_admin = authorise_as_admin()

        if not is_admin and str(review.user_id) != get_jwt_identity():
            return {"error": "User is not authorised to perform this action."}, 403

        db.session.delete(review)
        db.session.commit()
        return {"message": f"Review '{review.review_title}' deleted successfully"}
    
    else:
        return {"error": f"Review with id {review_id} not found"}, 404

@reviews_bp.route("/reviews/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_review(school_id, review_id):
    body_data = review_schema.load(request.get_json())

    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    if review:
        if str(review.user_id) != get_jwt_identity():
            return {"error": "You are not the owner of the review"}, 403 

        review.review_title = body_data.get("review_title") or review.review_title
        review.review_content = body_data.get("review_content") or review.review_content
    
        db.session.commit()
      
        return review_schema.dump(review)

    else:
        return {"error": f"Revuew with id {review_id} not found"}, 404