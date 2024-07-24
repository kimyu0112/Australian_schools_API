import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

def authorise_as_admin():

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
def auth_as_admin_decorator(fn):
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
                "error": "User account does not have admin privilleges to perform this operation"
            }, 403

    return wrapper
