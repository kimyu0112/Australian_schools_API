from init import db, ma
from marshmallow import fields
from sqlalchemy.sql import func

import datetime

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
    user = fields.Nested('UserSchema', only=["user_name"])
    school = fields.Nested('SchoolSchema', only=["school_name"])

    class Meta:
        fields = ("id", "review_title", "review_content", "created_at_time", "user", "school")
        ordered = True

reviews_schema = ReviewSchema(many=True)
review_schema = ReviewSchema()