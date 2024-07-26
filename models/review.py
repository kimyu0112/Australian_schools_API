import datetime

from init import db, ma
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow.validate import Length, And, Regexp, OneOf

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    review_title = db.Column(db.String, nullable=False)
    review_content = db.Column(db.String, nullable=False)
    created_at_time = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    school = db.relationship('School', back_populates='reviews')

class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "user_name"])
    school = fields.Nested('SchoolSchema', only=["id", "name"])

    review_title = fields.String(required=True, validate=And(
        Length(min=6, error="Title must be at least 6 characters long."),
        Regexp('^[A-Za-z0-9 ]+$', error="Alphanumeric characters only")
    ))

    review_content = fields.String(required=True, validate=Length(min=6, error="Review must be at least 6 characters long."))

    class Meta:
        fields = ("id", "review_title", "review_content", "created_at_time", "user", "school")
        ordered = True

reviews_schema = ReviewSchema(many=True)
review_schema = ReviewSchema()