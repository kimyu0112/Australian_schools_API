from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.school import School, school_schema, schoolss_schema
from controllers.review_controller import reviews_bp

schools_bp = Blueprint("schools", __name__, url_prefix="/schools")
schools_bp.register_blueprint(reviews_bp)

@schools_bp.route("/")
def get_all_schools():
    stmt = db.select(School).order_by(School.school_name().desc())
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

@schools_bp.route("/", methods=["POST"])
# @jwt_required()
def create_school():
 
    body_data = request.get_json()
   
    school = School(
        school_name=body_data.get("school_name"),
        contact_email=body_data.get("contact_email"),
        state=body_data.get("state"),
        suburb=body_data.get("suburb"),
        education_level=body_data.get("education_level"),
        sector=body_data.get("sector"),
        total_enrolment=body_data.get("total_enrolment"),
        state_overall_score=body_data.get("state_overall_score")
    )

    db.session.add(school)
    db.session.commit()
   
    return school_schema.dump(school)

# /cards/<id> - DELETE - delete a card
@schools_bp.route("/<int:school_id>", methods=["DELETE"])
# @jwt_required()
def delete_school(school_id):
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)
    if school:
        db.session.delete(school)
        db.session.commit()
        return {"message": f"School '{school.school_name}' deleted successfully"}
    else:
        return {"error": f"School with id {school_id} not found"}, 404
    

@schools_bp.route("/<int:school_id>", methods=["PUT", "PATCH"])
# @jwt_required()
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
        school.sector=body_data.get("sector") or school.sector
        school.total_enrolment=body_data.get("total_enrolment") or school.total_enrolment
        school.state_overall_score=body_data.get("state_overall_score") or school.state_overall_score

        db.session.commit()

        return school_schema.dump(school)
    else:
        return {"error": f"School with id {school_id} not found"}, 404