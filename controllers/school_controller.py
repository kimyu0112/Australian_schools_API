from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.school import School, school_schema, schools_schema
from controllers.review_controller import reviews_bp
from controllers.recent_event_controller import recent_events_bp
from controllers.school_subject_controller import school_subjects_bp
from utils import auth_as_admin_decorator

schools_bp = Blueprint("schools", __name__, url_prefix="/schools")
schools_bp.register_blueprint(recent_events_bp)
schools_bp.register_blueprint(school_subjects_bp)

@schools_bp.route("/")
def get_all_schools():
    stmt = db.select(School).order_by(School.school_name)
    schools = db.session.scalars(stmt)
    return schools_schema.dump(schools)

@schools_bp.route("/<int:school_id>")
def get_one_school(school_id):
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)
    if school:
        return school_schema.dump(school)
    else:
        return {"error": f"School with id {school_id} not found"}, 404

@schools_bp.route("/", methods=["POST"]) # admin needed
@jwt_required()
@auth_as_admin_decorator
def create_school():
    body_data = request.get_json()
   
    school = School(
        school_name=body_data.get("school_name"),
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


@schools_bp.route("/<int:school_id>", methods=["DELETE"]) # admin needed
@jwt_required()
@auth_as_admin_decorator
def delete_school(school_id):
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)
    if school:
        db.session.delete(school)
        db.session.commit()
        return {"message": f"School '{school.school_name}' deleted successfully"}
    else:
        return {"error": f"School with id {school_id} not found"}, 404
    

@schools_bp.route("/<int:school_id>", methods=["PUT", "PATCH"]) # admin needed
@jwt_required()
@auth_as_admin_decorator
def update_school(school_id):
    body_data = request.get_json()
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:
        school.school_name=body_data.get("school_name") or school.school_name
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