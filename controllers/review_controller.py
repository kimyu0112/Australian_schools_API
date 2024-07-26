from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.user import User
from models.school import School
from utils import auth_as_admin_decorator

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

# get all reviews
@reviews_bp.route("/all")
@jwt_required()
@auth_as_admin_decorator # only admin can access all reviews
def get_all_reviews():
    stmt = db.select(Review)
    reviews = db.session.scalars(stmt)

    return reviews_schema.dump(reviews)

# get one review
@reviews_bp.route("/<int:review_id>")
def get_one_review(review_id):

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)

    if review:
        return review_schema.dump(review)

    else:
        return {"error": f"Review with id {review_id} does not exist."}, 404
    
# delete one review
@reviews_bp.route("/<int:review_id>", methods=["DELETE"]) # only admin can delete review
@jwt_required()
@auth_as_admin_decorator
def delete_review(review_id):

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)

    if review:
        db.session.delete(review)
        db.session.commit()

        return {"message": f"Review '{review.review_title}' deleted successfully"}
        
    else:
        return {"error": f"Review with id {review_id} not found"}, 404

# get all reviews from one user
@reviews_bp.route("/users/<int:user_id>")
def retrieve_review_by_user_id(user_id):
    stmt_user = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt_user)

    if user:
        stmt_reviews = db.select(Review).filter_by(user_id=user_id)
        reviews = db.session.scalars(stmt_reviews)

        return reviews_schema.dump(reviews), 200
    
    else:
        return {"error": f"User account with ID {user_id} does not exist."}, 403

# get all reviews from one school
@reviews_bp.route("/schools/<int:school_id>")
def retrieve_review_by_school(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_reviews = db.select(Review).filter_by(school_id=school_id)
        reviews = db.session.scalars(stmt_reviews)
        return reviews_schema.dump(reviews), 200

    else:
        return {"error": f"School with id {school_id} is not found in the database."}, 404
    
# post one review on school with id school_id
@reviews_bp.route("/schools/<int:school_id>", methods=["POST"]) # any user can post review
@jwt_required()
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

# update one review from school
@reviews_bp.route("/schools/<int:school_id>/<int:review_id>", methods=["PUT", "PATCH"]) # only account owner can edit review
@jwt_required()
def edit_review(school_id, review_id):
    body_data = review_schema.load(request.get_json(), partial=True)

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    stmt_review = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt_review)
        
    if school:
        if review:
            if review.school_id == school_id and review.user_id == int(get_jwt_identity()):
                review.review_title=body_data.get("review_title") or review.review_title
                review.review_content=body_data.get("review_content") or review.review_content
                review.user_id=int(get_jwt_identity())
                review.school_id=review.school_id

                db.session.commit() 
      
                return review_schema.dump(review)
            
            else:
                return {"error": "This review belongs to another school or you are not authorised to update this review."}
        else:
            return {"error": f"Review with id {review_id} not found"}, 404
    else:
        return {"error": f"School with id {school_id} not found."}, 404
