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
    total_enronment = db.Column(db.String)
    state_overall_score = db.Column(db.Integer)

class SchoolSchema(ma.Schema):
    follows = fields.List(fields.Nested('FollowSchema'), exclude=["school"])
    class Meta:
        fields = ("id", "school_name", "coontact_email", "state", "suburb", "education_level", "sector", "total_enronment", "state_overall_score", "follows")

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)