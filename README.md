## LDSG (Local Development Setup Guide)

### Prerequisite

- #### Have python3 installed

### Steps to setup and run application on local development pc

- Navigate into project root

        cd drf_social/tradecore

- Once you are in the root project, Next steps, create virtual environment and activate it:

        python3 -m venv venv
        source venv/bin/activate


- Install dependencies

        pip install -r requirements.txt

- Run migrations and runserver

        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver

- Check running server on this port: http://127.0.0.1:8000/

        You will get API documentations with Swagger

- Create superadmin in your project terminal:

        python manage.py createsuperuser

- From root url, this one http://127.0.0.1:8000/:

        Create couple of datas

- Run unit tests with one of below commands:

        pytest
        python -m pytest

- Navigate to admin: http://127.0.0.1:8000/admin to view all your entries
