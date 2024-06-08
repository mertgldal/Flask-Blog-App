# Flask Blog Project

This project is a dynamic web application built using Flask, a lightweight Python web framework. It features user authentication, CRUD (Create, Read, Update, Delete) operations for blog posts, a commenting system, and a contact form for user inquiries via email.

[Project link](https://flask-blog-app-1-r3sx.onrender.com/)

## Features

- **User Authentication:** Secure registration, login, and logout functionality.
- **Blog Post Management:** Users can create, read, update, and delete their blog posts.
- **Commenting System:** Users can add comments to blog posts.
- **Contact Form:** Allows users to send messages via email.
- **Admin Role:** Special privileges for the admin to manage all blog posts and comments.
- **Flask Extensions:** Utilizes SQLAlchemy for ORM, Flask-Bootstrap for responsive design, CKEditor for rich text editing, and Flask-Gravatar for user avatars.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** Flask-Bootstrap, CKEditor
- **Extensions:** Flask-Login, Flask-WTF, Flask-Gravatar
- **Email:** smtplib, dotenv for environment variable management

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory of the project and add your environment variables:
   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///posts.db
   contact_email=your_email@example.com
   contact_email_pwd=your_email_password
   contact_mailbox=recipient_email@example.com
   ```

5. **Create the database:**
   ```bash
   flask shell
   >>> from models import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Run the application:**
   ```bash
   flask run
   ```
   Access the application in your web browser at `http://localhost:5000`.

## Usage

- **Home Page:** View all blog posts.
- **Post Details:** Click on a post to view details and comments.
- **Register/Login:** Register a new account or log in to an existing account.
- **Create/Edit/Delete Post:** After logging in, create new posts or edit/delete existing ones.
- **Comments:** Add comments to posts.
- **Contact:** Use the contact form to send an email message.

## Admin Role

- The first registered user is assigned the admin role (user ID 1).
- **Admin Privileges:**
  - Create, edit, and delete any blog post.
  - Delete any comment.
  - Access to admin-specific routes such as managing all posts and comments.

## Application Structure

```plaintext
.
├── .venv                   # Virtual environment
├── main.py                 # Main application file
├── models.py               # Database models
├── routes.py               # Application routes
├── forms.py                # Forms for user input
├── templates               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── post.html
│   ├── make-post.html
│   ├── about.html
│   ├── contact.html
│   ├── coming-soon.html
│   ├── header.html
│   └── footer.html
├── static                  # Static files (CSS, JS, images)
│   ├── css
│   └── js
├── .env                    # Environment variables
└── README.md               # Project documentation
```

- **main.py:** The main application script.
- **models.py:** Contains SQLAlchemy models for User, BlogPost, and Comment.
- **routes.py:** Defines the routes/endpoints for the application.
- **forms.py:** Defines WTForms for user registration, login, post creation, and comments.
- **templates/:** Contains HTML templates for different routes.
- **static/:** Contains static files such as CSS and JavaScript.
- **.env:** Environment variables for sensitive information.

## TODO
- Add a user profile page
- Add comment editing functionality
- Add reply functionality to comments

## Contributing

Contributions are welcome! Here are some ways you can help:

- Reporting bugs and opening issues.
- Submitting pull requests for new features or bug fixes.
- Improving documentation.

Please fork the repository and use a feature branch for your contributions. 

## Contact

For any questions or issues, please contact [mertguldal@outlook.com](mailto:mertguldal@outlook.com).
