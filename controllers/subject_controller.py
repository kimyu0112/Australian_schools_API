from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.subject import Subject, subject_schema, subjects_schema

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")

@subjects_bp.route("/")
def retrieve_all_subjects():
    stmt = db.select(Subject).order_by(Subject.subject_name())
    subjects = db.session.scalars(stmt)
    return subjects_schema.dump(subjects), 200


@subjects_bp.route("/", methods=["POST"]) #admin right needed
# @jwt_required()
def create_subject():
    body_data = request.get_json() 
    
    subject = Subject(
        subject_name=body_data.get("subject_name")
    )

    db.session.add(subject)
    db.session.commit()

    return subject_schema.dump(subject)

@subjects_bp.route("/<int:subject_id>/", methods=["DELETE"]) # admin right needed
# @jwt_required()
def delete_subject(subject_id):
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt)

    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {"message": f"Subject id {subject_id} deleted successfully"}

    else:
        return {"error": f"Subject with id {subject_id} not found."}, 404

            