from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.school import School
from models.school_subject import SchoolSubject, school_subject_schema, school_subjects_schema

school_subjects_bp = Blueprint("school_subjects", __name__, url_prefix="/<int:school_id>/subjects")

# retrieve all subjects by school id

@school_subjects_bp.route("/")
def get_all_subjects_by_school(school_id):

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_school_subject = db.select(school_subjects).filter_by(school_id=school_id)
        subjects = db.session.scalars(stmt_school_subject)
        return school_subjects_schema.dump(subjects)

    else:
        return {"error": f"School with id {school_id} not found."}, 404

# post a subject to school connection
@school_subjects_bp.route("/", methods=["POST"]) # admin right needed
def create_subject_taught_by_school(school_id):

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        body_data = request.get_json()

        school_subject = SchoolSubject (
            school_id=school_id,
            subject_id=body_data.get("subject_id")
        )

        db.session.add(school_subject)
        db.session.commit()

        return school_subject_schema.dump(school_subject), 201

    else:
        return {"error": f"School with id {school_id} not found."}, 404

# delete a subject to school connection
@school_subjects_bp.route("/<school_subject_id>", methods=["DELETE"]) # admin right needed
def delete_subject_taught_by_school(school_id, school_subject_id):
    stmt = db.select(SchoolSubject).filter_by(id=school_subject_id)
    school_subject = db.session.scalar(stmt)

    if school_subject:
        db.session.delete(school_subject)
        db.session.commit()

        return {"message": f"Connection {school_subject_id} removed successfully"}

    else:
        return {"error": f"Connection {school_subject_id} does not exist"}, 404