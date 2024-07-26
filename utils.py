import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User


def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
       
        if user == None:
            return {"error": "The logged in user has been deleted. Please sign up and apply for a new admin account and try again."}, 403

        elif user.is_admin:
            return fn(*args, **kwargs)
        
        else:
            return {"error": "Only admin can perform this action."}, 403

    return wrapper

# Decorator function to check whether user is an admin
def auth_as_admin_decorator_with_user_id(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        current_user_id = int(get_jwt_identity())
        stmt_user_from_token = db.select(User).filter_by(id=current_user_id)
        user_from_token = db.session.scalar(stmt_user_from_token)

        user_id = kwargs.get("user_id")
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        if user:
            if user_from_token:
                if user_from_token.is_admin:
                    return fn(*args, **kwargs)
                else:
                    return {"error": "You do not have the authorization to perform this operation"}, 403
            else:
                return {"error": "The logged in user has been deleted. Please sign up and apply for a new admin account and try again."}, 403
        else: 
            return {"error": f"User account with ID '{user_id}' does not exist"}, 403

    return wrapper


def account_owner_or_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        current_user_id = int(get_jwt_identity())
        stmt_user_from_token = db.select(User).filter_by(id=current_user_id)
        user_from_token = db.session.scalar(stmt_user_from_token)

        user_id = kwargs.get("user_id")
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        if user:
            if user_from_token:
                if user.id == current_user_id or user_from_token.is_admin:
                    return fn(*args, **kwargs)
                else:
                    return {"error": "You do not have the authorization to perform this operation"}, 403
            else:
                return {"error": "The logged in user has been deleted. Please sign up a new account and try again."}, 403
        else: 
            return {"error": f"User account with ID '{user_id}' does not exist"}, 403

    return wrapper


def account_owner_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        current_user_id = int(get_jwt_identity())
        stmt_user_from_token = db.select(User).filter_by(id=current_user_id)
        user_from_token = db.session.scalar(stmt_user_from_token)

        user_id = kwargs.get("user_id")
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        if user:
            if user_from_token:
                if user.id == current_user_id:
                    return fn(*args, **kwargs)
                else:
                    return {"error": "You do not have the authorization to perform this operation"}, 403
            else:
                return {"error": "The logged in user has been deleted. Please sign up a new account."}, 403
        else: 
            return {"error": f"User account with ID '{user_id}' does not exist"}, 403

    return wrapper    

