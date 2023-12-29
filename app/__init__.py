from flask import Flask
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .db.connection import db
    db.init_app(app)

    @app.route("/")
    def index():
        return "<h1>Hello World in Flask</h1>"

    from .apis import teachers
    app.register_blueprint(teachers.bp)
    from .apis import evaluations
    app.register_blueprint(evaluations.bp)

    with app.app_context():
        db.create_all()

    return app
