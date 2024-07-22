import datetime

from init import db, ma
from marshmallow import fields
from sqlalchemy.sql import func

class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    created_at_time = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    user = db.relationship('User', back_populates='follows')
    school = db.relationship('School', back_populates='follows')

class FollowSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "user_name"])
    school = fields.Nested('SchoolSchema', only=["school_name"])
    class Meta:
        fields = ("id", "user", "school", "created_at_time")

follows_schema = FollowSchema(many=True)
follow_schema = FollowSchema()