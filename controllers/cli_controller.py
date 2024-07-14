from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.follow import Follow
from models.school import School

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
            email="admin@email.com",
            password=bcrypt.generate_password_hash("168891").decode("utf-8"),
            is_admin=True
        ),
        User(
            user_name="kimyu0112",
            email="kimyu0112@outlook.com",
            password=bcrypt.generate_password_hash("168891").decode("utf-8"),
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
            sector="Government",
            total_enrolnment=964,
            state_overall_score=96
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
        )
    ]
    
    db.session.add_all(follows)

    db.session.commit()

    print("Tables seeded")



