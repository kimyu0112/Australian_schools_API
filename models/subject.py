from init import db, ma
from marshmallow import fields

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String, nullable=False)

    school_subjects = db.relationship('SchoolSubject', back_populates='subject')

class SubjectSchema(ma.Schema):
    school_subjects = fields.List(fields.Nested('SchoolSubjectSchema'), exclude=["subject"])
    class Meta:
        fields = ("id", "subject_name", "school_subjects")

subjects_schema = SubjectSchema(many=True)
subject_schema = SubjectSchema()