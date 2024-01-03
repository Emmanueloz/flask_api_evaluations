from flask import Flask

from app.db.db_users import add_user, query_user
from .config import Config
from .jwt import jwtm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .db.connection import db
    db.init_app(app)
    jwtm.init_app(app)

    @app.route("/")
    def index():
        return "<h1>Hello World in Flask</h1>"

    from .apis import teachers
    app.register_blueprint(teachers.bp)

    from .apis import evaluations
    app.register_blueprint(evaluations.bp)

    from .apis import auth
    app.register_blueprint(auth.bp)

    from .apis import teacher_profile
    app.register_blueprint(teacher_profile.bp)

    from .apis import users
    app.register_blueprint(users.bp)

    with app.app_context():
        user, error = query_user("admin")
        if user is None and error is not None:
            data_user = {
                "username": "admin",
                "email": "admin@email.com",
                "passwd": "123",
                "rol": "admin",
                "id_teacher": None
            }
            new_user = add_user(data_user)
            print(new_user)
        db.create_all()

    return app
