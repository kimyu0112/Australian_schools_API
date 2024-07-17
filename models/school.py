from init import db, ma
from marshmallow import fields

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    education_level = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=False)
    total_enrolment = db.Column(db.Integer)
    state_overall_score = db.Column(db.Integer)

    follows = db.relationship('Follow', back_populates='school', cascade="all, delete")
    reviews = db.relationship('Review', back_populates='school', cascade="all, delete")

class SchoolSchema(ma.Schema):
    follows = fields.List(fields.Nested('FollowSchema'), exclude=["school"])
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=["school"])
    class Meta:
        fields = ("id", "school_name", "contact_email", "state", "suburb", "education_level", "sector", "total_enrolnment", "state_overall_score", "follows", "reviews")

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)