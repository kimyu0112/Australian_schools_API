from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# VALID_STATES = ("New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia", "Tasmania", "Northern Territory", "Australian Capital Territory")
# VALID_SCHOOL_TYPES = ("Government School", "Private School", "Independent School", "Catholic School")

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    education_level = db.Column(db.String, nullable=False)
    school_type = db.Column(db.String, nullable=False)
    total_enrolment = db.Column(db.Integer)
    state_overall_score = db.Column(db.Integer)

    follows = db.relationship('Follow', back_populates='school', cascade="all, delete")
    reviews = db.relationship('Review', back_populates='school', cascade="all, delete")
    recent_events = db.relationship('Event', back_populates='school', cascade="all, delete")
    school_subjects = db.relationship('SchoolSubject', back_populates='school')

class SchoolSchema(ma.Schema):
    follows = fields.List(fields.Nested('FollowSchema'), exclude=["school"])
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=["school"])
    recent_events = fields.List(fields.Nested('EventSchema'), exclude=["school"])
    school_subjects = fields.List(fields.Nested('SchoolSubjectSchema'), exclude=["school"])

    # state = fields.String(validate=OneOf(VALID_STATES))
    # school_type = fields.String(validate=OneOf(VALID_SCHOOL_TYPES))

    class Meta:
        fields = ("id", "school_name", "contact_email", "state", "suburb", "education_level", "school_type", "total_enrolment", "state_overall_score", "follows", "reviews", "recent_events", "school_subjects")

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)