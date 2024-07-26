from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema, follows_schema
from models.school import School
from utils import auth_as_admin_decorator, account_owner_or_admin_decorator

follows_bp = Blueprint("follows", __name__, url_prefix="/follows")

# get all follows from one user
@follows_bp.route("/users/<int:user_id>") 
@jwt_required()
@account_owner_or_admin_decorator # admin or account owner
def get_user_follows(user_id):
    stmt = db.select(Follow).filter_by(user_id=user_id)
    follows = db.session.scalars(stmt)

    return follows_schema.dump(follows)
    
# get all follows
@follows_bp.route("/all") 
@jwt_required()
@auth_as_admin_decorator # admin
def get_all_follows():
    stmt = db.select(Follow)
    follows = db.session.scalars(stmt)

    return follows_schema.dump(follows)

# follow a school
@follows_bp.route("/schools/<int:school_id>", methods=["POST"])
@jwt_required()
def create_follow(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        
        stmt = db.select(Follow).filter_by(school_id=school_id, user_id=get_jwt_identity())
        follow_db = db.session.scalar(stmt)

        if follow_db:
            return {"message": "You have already followed this school"}
        
        else: 
            follow = Follow(
            user_id=int(get_jwt_identity()),
            school_id=school_id
        )

            db.session.add(follow)
            db.session.commit()

            return follow_schema.dump(follow)

    else:
        return {"error": f"School with id {school_id} not found"}, 404

# unfollow a school
@follows_bp.route("/schools/<int:school_id>/<int:follow_id>", methods=["DELETE"])
@jwt_required()
def delete_follow(school_id, follow_id):

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    stmt = db.select(Follow).filter_by(id=follow_id)
    follow = db.session.scalar(stmt)

    if school:
        if follow:
            if follow.school_id == school_id and follow.user_id == int(get_jwt_identity()):
                db.session.delete(follow)
                db.session.commit()
                return {"message": f"You have unfollowed {school.name}."}
            else:
                return {"error": "This follow belongs to another school or you are not authorised to delete this review."}
        
        else:
            return {"error": f"Follow with id {follow_id} not found"}, 404

    else:
        return {"error": f"School with id {school_id} not found"}, 404
