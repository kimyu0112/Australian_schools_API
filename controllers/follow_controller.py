from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema
from models.school import School

follows_bp = Blueprint("follows", __name__, url_prefix="/<int:school_id>/follows")

# we already get the follows while fetching schools, so, no need for "get follows" route here

# follow a school
@follows_bp.route("/", methods=["POST"])
@jwt_required()
def create_follow(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        
        stmt_follow_db = db.select(Follow).filter_by(school_id=school_id, user_id=int(get_jwt_identity()))
        follow_db = db.session.scalar(stmt_follow_db)

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
@follows_bp.route("/<int:follow_id>", methods=["DELETE"])
@jwt_required()
def delete_follow(school_id, follow_id):

    stmt = db.select(Follow).filter_by(id=follow_id)
    follow = db.session.scalar(stmt)

    if follow:
        db.session.delete(follow)
        db.session.commit()

        return {"message": f"You have unfollowed this school."}
        
    else:
        return {"error": f"Follow with id {follow_id} not found"}, 404

   
