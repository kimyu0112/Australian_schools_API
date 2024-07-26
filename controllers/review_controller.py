from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema
from models.school import School
from utils import auth_as_admin_decorator

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:school_id>/reviews")

# we already get the reviews while fetching schools, so, no need for "get reviews" route here

# get one review
@reviews_bp.route("/<int:review_id>")
def get_one_review(school_id, review_id):

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)

    if review:
        return review_schema.dump(review)

    else:
        return {"error": f"Review with id {review_id} does not exist."}, 404
    
# post one review
@reviews_bp.route("/", methods=["POST"]) 
@jwt_required() # any user can post review
def create_review(school_id):
    body_data = review_schema.load(request.get_json(), partial=True)

    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:

        review = Review(
            review_title=body_data.get("review_title"),
            review_content=body_data.get("review_content"),
            user_id=int(get_jwt_identity()),
            school_id=school_id
        )
    
        db.session.add(review)
        db.session.commit()

        return review_schema.dump(review), 201

    else:
        return {"error": f"School with id {school_id} not found."}, 404

# update one review
@reviews_bp.route("/<int:review_id>", methods=["PUT", "PATCH"]) # only account owner can edit review
@jwt_required()
def edit_review(school_id, review_id):
    body_data = review_schema.load(request.get_json(), partial=True)

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)
        
    if review:
        if review.user_id == int(get_jwt_identity()):
            review.review_title=body_data.get("review_title") or review.review_title
            review.review_content=body_data.get("review_content") or review.review_content
            review.user_id=int(get_jwt_identity())
            review.school_id=review.school_id

            db.session.commit() 
      
            return review_schema.dump(review)
            
        else:
            return {"error": "You are not authorised to update this review."}
    else:
        return {"error": f"Review with id {review_id} not found"}, 404

# delete one review
@reviews_bp.route("/<int:review_id>", methods=["DELETE"]) # only admin can delete review
@jwt_required()
@auth_as_admin_decorator
def delete_review(school_id, review_id):

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)

    if review:
        db.session.delete(review)
        db.session.commit()

        return {"message": f"Review with id {review_id} deleted successfully"}
        
    else:
        return {"error": f"Review with id {review_id} not found"}, 404
