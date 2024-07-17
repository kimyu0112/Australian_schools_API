from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.follow import Follow, follow_schema, follows_schema

follows_bp = Blueprint("follows", __name__, url_prefix="/follows")

@follows_bp.route("/")
def get_all_follows():
    stmt = db.select(Follow)
    follows = db.session.scalars(stmt)
    return follows_schema.dump(follows)

# @follows_bp.route("/<int:follow_id>")
# def get_one_follow(follow_id):
#     stmt = db.select(Follow).filter_by(id=follow_id)
#     follow = db.session.scalar(stmt)
#     if follow:
#         return follow_schema.dump(follow)
#     else:
#         return {"error": f"Follow with id {follow_id} not found"}, 404

@follows_bp.route("/", methods=["POST"])
@jwt_required()
def create_follow():
    body_data = request.get_json()
    follow = Follow(
        user_id=get_jwt_identity(),
        school_id=body_data.get("school_id")
    )
    db.session.add(follow)
    db.session.commit()
    return follow_schema.dump(follow)

@follows_bp.route("/<int:follow_id>", methods=["DELETE"])
@jwt_required()
def delete_follow(follow_id):
    stmt = db.select(Follow).filter_by(id=follow_id)
    follow = db.session.scalar(stmt)
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return {"message": f"Follow {follow.id} deleted successfully"}
    else:
         return {"error": f"Follow with id {follow_id} not found"}, 404