from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from controllers.recent_event_controller import recent_events_bp
from controllers.follow_controller import follows_bp
from controllers.review_controller import reviews_bp
from controllers.school_subject_controller import school_subjects_bp
from models.school import School, school_schema, schools_schema
from utils import auth_as_admin_decorator

schools_bp = Blueprint("schools", __name__, url_prefix="/schools")

schools_bp.register_blueprint(recent_events_bp)
schools_bp.register_blueprint(follows_bp)
schools_bp.register_blueprint(reviews_bp)
schools_bp.register_blueprint(school_subjects_bp)


# get all schools
@schools_bp.route("/all")
def get_all_schools():
    stmt = db.select(School).order_by(School.name)
    schools = db.session.scalars(stmt)

    return schools_schema.dump(schools)

# get one school
@schools_bp.route("/<int:school_id>")
def get_one_school(school_id):
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:
        return school_schema.dump(school)
    
    else:
        return {"error": f"School with id {school_id} not found"}, 404

# post one school
@schools_bp.route("/", methods=["POST"]) 
@jwt_required()
@auth_as_admin_decorator # admin needed
def create_school():
    try:
        body_data = request.get_json()

        school = School(
            name=body_data.get("name"),
            contact_email=body_data.get("contact_email"),
            state=body_data.get("state"),
            suburb=body_data.get("suburb"),
            education_level=body_data.get("education_level"),
            school_type=body_data.get("school_type"),
            total_enrolment=body_data.get("total_enrolment"),
            state_overall_score=body_data.get("state_overall_score")
        )

        db.session.add(school)
        db.session.commit()
    
        return school_schema.dump(school)

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"school_name already exists"}, 409

# update one school
@schools_bp.route("/<int:school_id>", methods=["PUT", "PATCH"]) 
@jwt_required()
@auth_as_admin_decorator # admin needed
def update_school(school_id):
    try:
        body_data = request.get_json()

        stmt = db.select(School).filter_by(id=school_id)
        school = db.session.scalar(stmt)

        if school:
            school.name=body_data.get("name") or school.name
            school.contact_email=body_data.get("contact_email") or school.contact_email
            school.state=body_data.get("state") or school.state
            school.suburb=body_data.get("suburb") or school.suburb
            school.education_level=body_data.get("education_level") or school.education_level
            school.school_type=body_data.get("school_type") or school.school_type
            school.total_enrolment=body_data.get("total_enrolment") or school.total_enrolment
            school.state_overall_score=body_data.get("state_overall_score") or school.state_overall_score

            db.session.commit()

            return school_schema.dump(school)
        
        else:
            return {"error": f"School with id {school_id} not found"}, 404

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"school_name already exists."}, 409

# delete one school
@schools_bp.route("/<int:school_id>", methods=["DELETE"]) 
@jwt_required()
@auth_as_admin_decorator # admin needed
def delete_school(school_id):
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:
        db.session.delete(school)
        db.session.commit()

        return {"message": f"School with id {school_id} deleted successfully"}
    
    else:
        return {"error": f"School with id {school_id} not found."}, 404


