import logging

from flask_bootstrap import Bootstrap
from flask import current_app, Flask, redirect, url_for, session
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_login import LoginManager

# oauth2 = UserOAuth2()
bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
migrate = Migrate()
# login.login_view = 'login'
# login.login_message = ('U moet eerst inloggen om deze pagina te kunnen bezoeken.')


def create_app(config, debug = False, testing = False, config_overrides = None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level = logging.INFO)

    # Setup the data model.

    login.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the Profile CRUD blueprint.
    from .routes import bp
    app.register_blueprint(bp, url_prefix = '/')

    # Add a default root route.
    # @app.route("/")
    # def index():
    #     return redirect(url_for('home'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
