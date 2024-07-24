from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import bcrypt, db
from models.user import User, UserSchema, user_schema, users_schema
from controllers.follow_controller import follows_bp
from utils import authorise_as_admin, auth_as_admin_decorator

users_bp = Blueprint("users", __name__, url_prefix="/users")
users_bp.register_blueprint(follows_bp)

@users_bp.route("/") #admin
@jwt_required()
@auth_as_admin_decorator
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return users_schema.dump(users)

@users_bp.route("/<int:user_id>") # need account owner or admin
@jwt_required()
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        is_admin = authorise_as_admin()

        if not is_admin and str(user_id) != get_jwt_identity():
            return {"error": "You are not authorised to perform this operation"}, 403 
        else:
            return user_schema.dump(user)
    else:
        return {"error": f"User id {user_id} does not exist"}

@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"]) # admin right or account owner
@jwt_required()
def update_user(user_id):
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    
    if user:
        is_admin = authorise_as_admin()

        if not is_admin and str(user_id) != get_jwt_identity():
            return {"error": "You are not authorised to perform this operation"}, 403

        else:
            user.user_name = body_data.get("user_name") or user.user_name
            user.email = body_data.get("email") or user.email

            password = body_data.get("password")

            if password:
                user.password = bcrypt.generate_password_hash(password).decode("utf-8")
            else:
                user.password

            db.session.commit()
       
            return user_schema.dump(user)
    
    else:
        return {"error": f"User id {user_id} does not exist"}

@users_bp.route("/<int:user_id>", methods=["DELETE"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id {user_id} deleted successfully"}, 200

    else:
        return {"error": f"User with id {user_id} not found"}, 404