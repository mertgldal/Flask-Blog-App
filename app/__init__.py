from flask import Flask
from app.extensions import db, login_manager, migrate, ckeditor, bootstrap, gravatar
from app.blueprints.routes import routes
from app.models.user import User
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    gravatar.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(routes)

    # Setup login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
