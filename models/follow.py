from init import db, ma
from marshmallow import fields
from sqlalchemy.sql import func

import datetime

class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    
    created_at_time = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # school_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='follows')

class FollowSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "user_name"])

    class Meta:
        fields = ("id", "user_id", "created_at_time")

follows_schema = FollowSchema(many=True)
follow_schema = FollowSchema()