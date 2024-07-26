from init import db, ma
from marshmallow import fields

class SchoolSubject(db.Model):
    __tablename__ = "school_subjects"

    id = db.Column(db.Integer, primary_key=True)

    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    subject = db.relationship('Subject', back_populates='school_subjects')
    school = db.relationship('School', back_populates='school_subjects')

class SchoolSubjectSchema(ma.Schema):
    subject = fields.Nested('SubjectSchema', only=["id", "subject_name"])
    school = fields.Nested('SchoolSchema', only=["id", "name"])

    class Meta:
        fields = ("id", "subject", "school")

school_subjects_schema = SchoolSubjectSchema(many=True)
school_subject_schema = SchoolSubjectSchema()
