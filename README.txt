# Social Network REST API

This project is a simple REST API based social network built with Django and Django REST Framework. Users can sign up, create text posts, view, like, and unlike other users' posts.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

2.Create a virtual environment:
python3 -m venv env
source env/bin/activate

3.Install the dependencies:
pip install -r requirements.txt

4.Set up the database (assuming PostgreSQL):
Create a new PostgreSQL database.
Update the database configuration in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

python manage.py migrate
python manage.py runserver

The API will be accessible at http://localhost:8000.

API Endpoints
User Signup: POST /api/signup/
User Login: POST /api/login/
Get User Data: GET /api/user/
Create a Post: POST /api/posts/
Retrieve, Update, or Delete a Post: GET/PUT/DELETE /api/posts/<post_id>/

python manage.py test

Additional Notes
This project uses JWT (JSON Web Token) for user authentication.
Asynchronous data enrichment is performed using the retry decorator.
Third-party APIs are used for email validation, geolocation data, and holiday checking.
