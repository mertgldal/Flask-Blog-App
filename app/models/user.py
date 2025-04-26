from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("BlogPost", back_populates="author")
    comments = db.relationship("Comment", back_populates="author")

    # Adding admin role to db
    role = db.Column(db.String(50), nullable=False, default="user", server_default="user")

    @property
    def is_admin(self):
        return self.role == 'admin'

    # TODO: Add new roles
    # @property
    # def is_moderator(self):
    #     return self.role == 'moderator'
