# Zoup
Django web app for food delivery and restaurant discovery.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Install Python
You'll need Python 3.0+ installed before installing and using this package. Recommended using the Python version in runtime.txt.

#### Install pipenv
Use the following command to install `pipenv`:
```shell script
pip install pipenv
```

#### Create virtualenv and Install Dependencies
Mount to project directory and run the following commands:
```shell script
cd ./path/to/zoup
pipenv shell
```
This should create a virtualenv and activate it. Install dependencies using:
```shell script
pipenv install
```
This will use Pipfile and Pipfile.lock to install project dependencies.

#### Create a Local Development Settings File
Create a file `local.py` in `zoup/settings` with the following code:
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('SECRET_KEY', 'g1onp1%knxzj-fvs3&eh@*9+*=oh7e&r-o70r36yz_zq68+cp*')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
```
This configuration will be used when running the app locally.

### Run the app
Use the following commands to run the app:
```shell script
python manage.py migrate
python manage.py loaddata zoup_app/fixtures/initial.json
python manage.py runserver
```