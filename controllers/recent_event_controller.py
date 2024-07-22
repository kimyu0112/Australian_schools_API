from flask import Blueprint, request

from init import db
from models.school import School, school_schema, schools_schema
from models.recent_event import Event, event_schema, events_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import authorise_as_admin

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

@recent_events_bp.route("/", methods=["POST"])
def create_recent_event(school_id):
    body_data = request.get_json() # to be checked
    
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


@recent_events_bp.route("/<int:event_id>/", methods=["DELETE"])
@jwt_required()
def delete_event(school_id, event_id):

    stmt_school = db.select(School).filter_by(id=school_id)
    school = db.session.scalar(stmt_school)

    if school:
        stmt_event = db.select(Event).filter_by(id=event_id)
        event = db.session.scalar(stmt_event)
        
    else:
        return {"error": f"School with id {school_id} not found."}, 404

    if event:
        is_admin = authorise_as_admin()
    else:
        return {"message": f"Event with {event_id} does not exist"}, 404

    if is_admin:
        db.session.delete(event)
        db.session.commit()
        return {"message": f"Event id {event_id} deleted successfully"}
    else:
        return {"message": "you are not authorised to perform this action"}, 403
            

# @reviews_bp.route("/reviews/<int:review_id>", methods=["PUT", "PATCH"])
# @jwt_required()
# def edit_review(school_id, review_id):
#     body_data = review_schema.load(request.get_json())

#     stmt = db.select(Review).filter_by(id=review_id)
#     review = db.session.scalar(stmt)

#     if review:
#         if str(review.user_id) != get_jwt_identity():
#             return {"error": "You are not the owner of the review"}, 403 

#         review.review_title = body_data.get("review_title") or review.review_title
#         review.review_content = body_data.get("review_content") or review.review_content
    
#         db.session.commit()
      
#         return review_schema.dump(review)

#     else:
#         return {"error": f"Revuew with id {review_id} not found"}, 404