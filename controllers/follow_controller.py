from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema, follows_schema
from models.user import User, user_schema

follows_bp = Blueprint("follows", __name__, url_prefix="/<int:user_id>/follows")

@follows_bp.route("/") # admin or account owner
# @jwt_required()
def get_all_follows(user_id):
    stmt_follow = db.select(Follow).filter_by(user_id=user_id)
    follows = db.session.scalars(stmt_follow)

    stmt_user = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt_user)

    if follows and user:
        return follows_schema.dump(follows)
    else:
        return {"message": f"User {user_id} does not exist or there are no followed schools"}, 404


@follows_bp.route("/", methods=["POST"]) # account owner
@jwt_required()
def create_follow(user_id):
    body_data = request.get_json()
    follow = Follow(
        user_id = get_jwt_identity(),
        school_id = body_data.get("school_id")
    )
    db.session.add(follow)
    db.session.commit()
    return follow_schema.dump(follow)

@follows_bp.route("/<int:follow_id>", methods=["DELETE"]) # account owner
@jwt_required()
def delete_follow(user_id, follow_id):
    stmt = db.select(Follow).filter_by(id=follow_id)
    follow = db.session.scalar(stmt)
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return {"message": f"Follow {follow.id} deleted successfully"}
    else:
         return {"error": f"Follow with id {follow_id} not found"}, 404