from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.follow import Follow
from models.school import School
from models.review import Review
from models.recent_event import Event
from models.subject import Subject
from models.school_subject import SchoolSubject

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            user_name="admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("168891").decode("utf-8"),
            is_admin=True
        ),
        User(
            user_name="kimyu0112",
            email="kimyu0112@outlook.com",
            password=bcrypt.generate_password_hash("168891").decode("utf-8"),
        ),
         User(
            user_name="hm09290929",
            email="hm09290929@outlook.com",
            password=bcrypt.generate_password_hash("333444").decode("utf-8"),
        )
    ]

    db.session.add_all(users)

    schools = [
        School(
            school_name="Brenwood Park Primary School",
            contact_email="brentwood.park.ps@education.vic.gov.au",
            state="Victoria",
            suburb="Berwick",
            education_level="Primary School",
            school_type="Government School",
            total_enrolment=964,
            state_overall_score=96
        ),
        School(
            school_name="Kambrya College",
            contact_email="kambrya@education.vic.government.au",
            state="Victoria",
            suburb="Berwick",
            education_level="Secondary School",
            school_type="Government School",
            total_enrolment=1226,
            state_overall_score=87
        )
    ]

    db.session.add_all(schools)

    follows = [
        Follow(
            user=users[1],
            school=schools[0]
        ),
        Follow(
            user=users[0],
            school=schools[0]
        ),
        Follow(
            user=users[0],
            school=schools[1]
        )
    ]
    
    db.session.add_all(follows)

    reviews = [
        Review(
            review_title="This school's Principal is good!",
            review_content="Blablabla",
            user=users[0],
            school=schools[0]
        ),
        Review(
            review_title="This school is bad!",
            review_content="Blablabla",
            user=users[0],
            school=schools[1]
        ),
        Review(
            review_title="Staff can be better supported",
            review_content="Blablabla",
            user=users[1],
            school=schools[1]
        )
    ]
    
    db.session.add_all(reviews)

    events = [
        Event(
            event_title="School open day is coming",
            event_brief_desciption="Blablabla",
            school=schools[0]
        ),
        Event(
            event_title="This school has achieved excelent ACE results",
            event_brief_desciption="Blablabla",
            school=schools[1]
        ),
        Event(
            event_title="This school has increased school fees",
            event_brief_desciption="Blablabla",
            school=schools[1]
        )
    ]

    db.session.add_all(events)

    db.session.commit()

    print("Tables seeded")



