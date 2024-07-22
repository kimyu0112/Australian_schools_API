from init import db, ma
from marshmallow import fields

class Event(db.Model):
    __tablename__ = "recent_events"

    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String, nullable=False)
    event_brief_desciption = db.Column(db.String, nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    school = db.relationship('School', back_populates='recent_events')

class EventSchema(ma.Schema):
    school = fields.Nested('SchoolSchema', only=["id", "school_name"])
    class Meta:
        fields = ("id", "event_title", "event_brief_desciption", "school")

events_schema = EventSchema(many=True)
event_schema = EventSchema()