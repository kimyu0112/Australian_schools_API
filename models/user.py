from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    follows = db.relationship('Follow', back_populates='user', cascade="all, delete")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete")

class UserSchema(ma.Schema):
    follows = fields.List(fields.Nested('FollowSchema'), exclude=["user"])
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=["user"])

    user_name = fields.String(required=True, validate=Regexp("^[0-9A-Za-z]{6,16}$", error="User name should contain only letters and numbers, and it must be between 6 and 16 characters long"))
    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))
    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Minimum eight characters, at least one letter and one number"))
    
    class Meta:
        fields = ("id", "user_name", "email", "password", "is_admin", "follows", "reviews")

users_schema = UserSchema(many=True, exclude=["password"])
user_schema = UserSchema(exclude=["password"])
