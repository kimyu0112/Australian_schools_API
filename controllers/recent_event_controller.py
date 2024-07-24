from flask import Blueprint, request

from init import db
from models.school import School, school_schema, schools_schema
from models.recent_event import Event, event_schema, events_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

recent_events_bp = Blueprint("recent_events", __name__, url_prefix="/<int:school_id>/recent_events")

@recent_events_bp.route("/")
def retrieve_recent_events_by_school(school_id):
    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_recent_events = db.select(Event).filter_by(school_id=school_id)
        recent_events = db.session.scalars(stmt_recent_events)
        return events_schema.dump(recent_events), 200

    else:
        return {"error": f"School with id {school_id} not found."}, 404

@recent_events_bp.route("/", methods=["POST"]) # admin needed
@jwt_required()
@auth_as_admin_decorator
def create_recent_event(school_id):
    body_data = request.get_json()
    
    stmt = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt)

    if school:
        event = Event(
            event_title=body_data.get("event_title"),
            event_brief_desciption=body_data.get("event_brief_desciption"),
            school=school
        )
    
        db.session.add(event)
        db.session.commit()

        return event_schema.dump(event), 201

    else:
        return {"error": f"School with id {school_id} not found."}, 404


@recent_events_bp.route("/<int:event_id>/", methods=["DELETE"]) # admin right needed
@jwt_required()
@auth_as_admin_decorator
def delete_event(school_id, event_id):

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_event = db.select(Event).filter_by(id=event_id)
        event = db.session.scalar(stmt_event)
        
    else:
        return {"error": f"School with id {school_id} not found."}, 404

    if event:
        db.session.delete(event)
        db.session.commit()
        return {"message": f"Event id {event_id} deleted successfully"}

    else:
        return {"message": f"Event with {event_id} does not exist"}, 404
            
@recent_events_bp.route("/<int:event_id>/", methods=["PUT", "PATCH"]) # admin
@jwt_required()
@auth_as_admin_decorator
def edit_event(school_id, event_id):
    body_data = event_schema.load(request.get_json())

    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        event.event_title_title = body_data.get("event_title") or event.event_title_title
        event.event_brief_desciption = body_data.get("event_brief_desciption") or event.event_brief_desciption

        school_id = school_id
    
        db.session.commit()
      
        return event_schema.dump(event)

    else:
        return {"error": f"Event with id {event_id} not found"}, 404