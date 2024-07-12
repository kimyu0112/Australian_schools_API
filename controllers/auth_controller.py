from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db

from models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = request.get_json()
        user = User(
            user_name=body_data.get("user_name"),
            email=body_data.get("email")
        )
        password=body_data.get("password")

        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 404
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address is already in use"}, 409


