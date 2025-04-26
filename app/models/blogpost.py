from app.extensions import db


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")

    # New feature for summary with AI
    summary = db.Column(db.Text, nullable=True)

    # New feature for view count and avg_read_time
    views = db.Column(db.Integer, default=0)
    avg_read_time = db.Column(db.Float, default=0.0)  # In minutes
