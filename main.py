from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_gravatar import Gravatar
from models import db, User
from routes import routes
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'sqlite:///posts.db')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

# Initialize extensions
db.init_app(app)
ckeditor = CKEditor(app)
Bootstrap5(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'
login_manager.refresh_view = 'routes.login'
login_manager.needs_refresh_message = 'Your password successfully changed.'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register blueprints
app.register_blueprint(routes)


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=False)
