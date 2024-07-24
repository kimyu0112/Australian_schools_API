from datetime import timedelta
import functools

from flask import Blueprint, request
# from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, get_jwt_identity

from init import bcrypt, db
from models.user import User, user_schema, UserSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = UserSchema().load(request.get_json())
        user = User(
            user_name=body_data.get("user_name"),
            email=body_data.get("email")
        )
        password = body_data.get("password")

        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201

    # except ValidationError as ve:
    #     return {"error": ve.messages}, 400
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # to be fixed
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # to be fixed
            return {"error": f"{err.orig.diag.column_name} is already in use"}, 409

@auth_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
 
        return {"email": user.email, "is_admin": user.is_admin, "token": token}

    else:
        return {"error": "Invalid user email or password"}, 401

def is_user_admin():

    # Get user_id from the JWT token
    user_id = int(get_jwt_identity())

    # Find the user record with the user_id
    # SELECT * FROM users where user_id = jwt_user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # For edge case where old JWT token is used for a deleted account
    if user is None:
        return {
            "error": "The logged in user has been deleted. Please login again."
        }, 403

    # Return True if user is admin, otherwise False
    return user.is_admin


# Decorator function to make sure user account is an admin
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Get user_id from the JWT token
        user_id = int(get_jwt_identity())

        # SELECT * FROM users where user_id = jwt_user_id
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # For edge case where old JWT token is used for a deleted account
        if user is None:
            return {
                "error": "The logged in user has been deleted. Please login again."
            }, 403

        # Run the decorated function if user is admin
        if user.is_admin:
            return fn(*args, **kwargs)

        # Else, return error that user is not an admin
        else:
            return {
                "error": "User account does not have admin privilleges"
            }, 403

    return wrapper