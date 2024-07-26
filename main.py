import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.follow_controller import follows_bp
    app.register_blueprint(follows_bp)

    from controllers.school_controller import schools_bp
    app.register_blueprint(schools_bp)

    from controllers.review_controller import reviews_bp
    app.register_blueprint(reviews_bp)

    from controllers.recent_event_controller import recent_events_bp
    app.register_blueprint(recent_events_bp)

    from controllers.user_controller import users_bp
    app.register_blueprint(users_bp)

    from controllers.subject_controller import subjects_bp
    app.register_blueprint(subjects_bp)

    from controllers.school_subject_controller import school_subjects_bp
    app.register_blueprint(school_subjects_bp)

    return app