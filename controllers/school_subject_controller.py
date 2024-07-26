from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.school import School
from models.subject import Subject
from models.school_subject import SchoolSubject, school_subject_schema, school_subjects_schema
from utils import auth_as_admin_decorator

school_subjects_bp = Blueprint("school-subjects", __name__)

# get all subjects per school
@school_subjects_bp.route("/schools/<int:school_id>/subjects")
def get_all_subjects_by_school(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_school_subject = db.select(SchoolSubject).filter_by(school_id=school_id)
        subjects = db.session.scalars(stmt_school_subject)
        return school_subjects_schema.dump(subjects)

    else:
        return {"error": f"School with id {school_id} not found."}, 404

# get all school_subject connections
@school_subjects_bp.route("/school-subjects/all")
@jwt_required()
@auth_as_admin_decorator
def get_all_school_subjects():
    stmt = db.select(SchoolSubject)
    school_subjects = db.session.scalars(stmt)

    return school_subjects_schema.dump(school_subjects)

# get one school_subject connections
@school_subjects_bp.route("/school-subjects/<int:school_subject_id>")
@jwt_required()
@auth_as_admin_decorator
def get_one_school_subject(school_subject_id):
    stmt = db.select(SchoolSubject).filter_by(id=school_subject_id)
    school_subject = db.session.scalar(stmt)

    return school_subject_schema.dump(school_subject)

# post a subject to school connection
@school_subjects_bp.route("/school-subjects", methods=["POST"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def create_subject_taught_by_school():

    body_data = request.get_json()

    school_id=body_data.get("school_id")
    subject_id=body_data.get("subject_id")

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    stmt_subject = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt_subject)

    if school:
        if subject:

            stmt = db.select(SchoolSubject).filter_by(school_id=school_id, subject_id=subject_id)
            schoolsubject_db = db.session.scalar(stmt)

            if schoolsubject_db:
                return {"message": "We already have this conection."}

            else:
                school_subject = SchoolSubject (
                school=school,
                subject_id=body_data.get("subject_id")
                )
                db.session.add(school_subject)
                db.session.commit()

            return school_subject_schema.dump(school_subject), 201

        else:
            return {"error": f"Subject with id {subject_id} not found."}, 404

    else:
        return {"error": f"School with id {school_id} not found."}, 404

# delete a subject to school connection
@school_subjects_bp.route("/school-subjects/<int:school_subject_id>", methods=["DELETE"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def delete_subject_taught_by_school(school_subject_id):
    stmt = db.select(SchoolSubject).filter_by(id=school_subject_id)
    school_subject = db.session.scalar(stmt)

    if school_subject:
        db.session.delete(school_subject)
        db.session.commit()

        return {"message": f"Connection {school_subject_id} removed successfully"}

    else:
        return {"error": f"Connection {school_subject_id} does not exist."}, 404