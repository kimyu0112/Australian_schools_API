from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

from init import bcrypt, db
from models.user import User, user_schema, UserSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# register a user
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = UserSchema().load(request.get_json(), partial=True)

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
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"Email or user_name already exists."}, 409

        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required."}, 409
    
# user login
@auth_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
        return {"email": user.email, "is_admin": user.is_admin, "token": token}

    else:
        return {"error": "Incorrect user email or password"}, 401