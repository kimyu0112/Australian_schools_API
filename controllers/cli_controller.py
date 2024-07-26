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
            password=bcrypt.generate_password_hash("Huber@123456").decode("utf-8"),
            is_admin=True
        ),
        User(
            user_name="user1234",
            email="user1234@outlook.com",
            password=bcrypt.generate_password_hash("Huber@234567").decode("utf-8"),
        ),
         User(
            user_name="huber2345",
            email="huber2345@outlook.com",
            password=bcrypt.generate_password_hash("Asdf@3579").decode("utf-8"),
        )
    ]

    db.session.add_all(users)

    schools = [
        School(
            name="Brenwood Park Primary School",
            contact_email="brentwood.park.ps@education.vic.gov.au",
            state="Victoria",
            suburb="Berwick",
            education_level="Primary School",
            school_type="Government School",
            total_enrolment=964,
            state_overall_score=96
        ),
        School(
            name="Kambrya College",
            contact_email="kambrya@education.vic.government.au",
            state="Victoria",
            suburb="Berwick",
            education_level="Secondary School",
            school_type="Government School",
            total_enrolment=1226,
            state_overall_score=87
        ),
        School(
            name="Berwick College",
            contact_email="berwickcollege@education.vic.government.au",
            state="Victoria",
            suburb="Berwick",
            education_level="Secondary School",
            school_type="Government School",
            total_enrolment=1888,
            state_overall_score=77
        ),

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
        ),
        Follow(
            user=users[1],
            school=schools[2]
        )
    ]
    
    db.session.add_all(follows)

    reviews = [
        Review(
            review_title="This school's Principal is good!",
            review_content="He is kind and carinig to his students.",
            user_id=1,
            school_id=1
        ),
        Review(
            review_title="This school should have more options for canteen food!",
            review_content="Canteen has not enought options for vegetarians.",
            user_id=1,
            school_id=2
        ),
        Review(
            review_title="Staff can be better supported",
            review_content="Not enough back up when teachers are sick.",
            user_id=2,
            school_id=2
        ),
        Review(
            review_title="Principal and his staff are excellent",
            review_content="Best school my kid has ever attended.",
            user_id=2,
            school_id=3
        )
    ]
    
    db.session.add_all(reviews)

    events = [
        Event(
            event_title="School open day is coming",
            event_brief_desciption="School open day will be next coming Monday xx/xx/2024.",
            school_id=1
        ),
        Event(
            event_title="This school has achieved excelent ACE results",
            event_brief_desciption="78% of out students achieved ATAR 90 and above",
            school_id=2
        ),
        Event(
            event_title="This school has increased school fees",
            event_brief_desciption="School fees have increased by 5%",
            school_id=2
        ),
        Event(
            event_title="This school has an upcoming book fair on 1/08/2024",
            event_brief_desciption="Please bring some money so your kid can purchase books of their interest.",
            school_id=3
        )
    ]
    
    db.session.add_all(events)

    subjects = [
        Subject(
            subject_name="Mathematics"
        ),
        Subject(
            subject_name="English Literature"
        ),
        Subject(
            subject_name="Physical Education"
        ),
        Subject(
            subject_name="Enquiry Learning"
        )
    ]
    
    db.session.add_all(subjects)

    school_subjects = [
        SchoolSubject(
            school=schools[1],
            subject=subjects[1]
        ),
        SchoolSubject(
            school=schools[1],
            subject=subjects[2]
        ),
        SchoolSubject(
            school=schools[0],
            subject=subjects[1]
        ),
        SchoolSubject(
            school=schools[2],
            subject=subjects[0]
        )
    ]

    db.session.add_all(school_subjects)

    db.session.commit()

    print("Tables seeded")



