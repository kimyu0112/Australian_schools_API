from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False,)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    follows = db.relationship('Follow', back_populates='user', cascade="all, delete")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete")

class UserSchema(ma.Schema):
    follows = fields.List(fields.Nested('FollowSchema'), exclude=["user"])
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=["user"])
    class Meta:
        fields = ("id", "user_name", "email", "password", "is_admin", "follows", "reviews")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])