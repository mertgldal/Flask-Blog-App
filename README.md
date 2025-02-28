# Flask Blog Project

This project is a dynamic web application built using Flask, a lightweight Python web framework. It features user authentication, CRUD (Create, Read, Update, Delete) operations for blog posts, a commenting system, and a contact form for user inquiries via email.

## Features

- **User Authentication:** Secure registration, login, and logout functionality.
- **Blog Post Management:** Users can create, read, update, and delete their blog posts.
- **Commenting System:** Users can add comments to blog posts.
- **Contact Form:** Allows users to send messages via email.
- **Admin Role:** Special privileges for the admin to manage all blog posts and comments.
- **Profile Page:** Users can view and update their profile, including changing their password.
- **Flask Extensions:** Utilizes SQLAlchemy for ORM, Flask-Bootstrap for responsive design, CKEditor for rich text editing, and Flask-Gravatar for user avatars.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** Flask-Bootstrap, CKEditor
- **Extensions:** Flask-Login, Flask-WTF, Flask-Gravatar
- **Email:** smtplib, dotenv for environment variable management

## Usage

- **Home Page:** View all blog posts.
- **Post Details:** Click on a post to view details and comments.
- **Register/Login:** Register a new account or log in to an existing account.
- **Create/Edit/Delete Post:** After logging in, create new posts or edit/delete existing ones.
- **Comments:** Add comments to posts.
- **Contact:** Use the contact form to send an email message.
- **Profile Page:** View and update your profile, including changing your password.

## Admin Role

- The first registered user is assigned the admin role (user ID 1).
- **Admin Privileges:**
  - Create, edit, and delete any blog post.
  - Delete any comment.
  - Access to admin-specific routes such as managing all posts and comments.

## Application Structure

```plaintext
my_flask_app/
├── my_flask_app/
│   ├── __init__.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── blogpost.py
│   │   ├── comment.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── post_form.py
│   │   ├── user_form.py
│   │   ├── comment_form.py
│   │   ├── contact_form.py
│   ├── templates/
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── make-post.html
│   │   ├── post.html
│   │   ├── profile-page.html
│   │   ├── register.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── extensions.py
│   ├── config.py
│   ├── main.py
├── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_models.py
├── .env
├── .flaskenv
├── requirements.txt
├── README.md
```

- **my_flask_app/__init__.py:** Initializes the Flask application and its extensions.
- **my_flask_app/blueprints/routes.py:** Defines the routes/endpoints for the application.
- **my_flask_app/models/:** Contains SQLAlchemy models for User, BlogPost, and Comment.
- **my_flask_app/forms/:** Defines WTForms for user registration, login, post creation, comments, and contact.
- **my_flask_app/templates/:** Contains HTML templates for different routes.
- **my_flask_app/static/:** Contains static files such as CSS and JavaScript.
- **my_flask_app/extensions.py:** Initializes Flask extensions.
- **my_flask_app/config.py:** Configuration settings for the Flask application.
- **my_flask_app/main.py:** The main application script.
- **migrations/:** Database migration files.
- **tests/:** Unit tests for the application.
- **.env:** Environment variables for sensitive information.
- **requirements.txt:** Lists the project's dependencies.
- **README.md:** Project documentation.

## TODO
- Add comment editing functionality
- Add reply functionality to comments
- Add profile page

## Contributing

Contributions are welcome! Here are some ways you can help:

- Reporting bugs and opening issues.
- Submitting pull requests for new features or bug fixes.
- Improving documentation.

Please fork the repository and use a feature branch for your contributions. 

## Contact

For any questions or issues, please [contact me](mailto:mertguldal@outlook.com).