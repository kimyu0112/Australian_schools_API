from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db
from models.user import User, UserSchema, user_schema, users_schema
from controllers.follow_controller import follows_bp
from utils import auth_as_admin_decorator, auth_as_admin_decorator_with_user_id, account_owner_or_admin_decorator

users_bp = Blueprint("users", __name__, url_prefix="/users")
users_bp.register_blueprint(follows_bp)

# get all users
@users_bp.route("/all") #admin
@jwt_required()
@auth_as_admin_decorator
def get_all_users():
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    stmt_users = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt_users)

    return users_schema.dump(users)

# get one user
@users_bp.route("/<int:user_id>") # account owner or admin
@jwt_required()
@account_owner_or_admin_decorator
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    return user_schema.dump(user)

# update one user
@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"]) # account owner or admin
@jwt_required()
@account_owner_or_admin_decorator
def update_user(user_id):
    try:
        body_data = UserSchema().load(request.get_json(), partial=True)
        password = body_data.get("password")
        
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        user.user_name = body_data.get("user_name") or user.user_name
        user.email = body_data.get("email") or user.email
        password = body_data.get("password")

        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        else:
            user.password

        db.session.commit()
        
        return user_schema.dump(user)
        
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"email or user_name you want to change to already exists."}, 409

# delete one user
@users_bp.route("/<int:user_id>", methods=["DELETE"]) # admin only
@jwt_required()
@auth_as_admin_decorator_with_user_id
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    db.session.delete(user)
    db.session.commit()

    return {"message": f"User with id {user_id} deleted successfully"}, 200