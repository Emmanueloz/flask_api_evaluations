from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "<h1>Hello World in Flask</h1>"

    from .apis import evaluations
    app.register_blueprint(evaluations.bp)

    return app
