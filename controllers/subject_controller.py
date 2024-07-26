from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.subject import Subject, subject_schema, subjects_schema
from utils import auth_as_admin_decorator

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")

# get all subjects
@subjects_bp.route("/all")
def retrieve_all_subjects():
    stmt = db.select(Subject).order_by(Subject.subject_name)
    subjects = db.session.scalars(stmt)

    return subjects_schema.dump(subjects)

# get one subject
@subjects_bp.route("/<int:subject_id>")
def retrieve_one_subject(subject_id):
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt)

    return subject_schema.dump(subject)

# post one subject
@subjects_bp.route("/", methods=["POST"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def create_subject():
    try:
        body_data = request.get_json()
    
        subject = Subject(
            subject_name=body_data.get("subject_name")
        )

        db.session.add(subject)
        db.session.commit()

        return subject_schema.dump(subject)

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"subject already exists."}, 409
            
# delete one subject
@subjects_bp.route("/<int:subject_id>/", methods=["DELETE"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def delete_subject(subject_id):
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt)

    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {"message": f"Subject id {subject_id} deleted successfully"}

    else:
        return {"error": f"Subject with id {subject_id} not found."}, 404
