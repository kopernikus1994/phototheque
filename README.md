# Phototheque

## Install python packages
- `pip install virtualenv`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

## Init db 
- `FLASK_APP=app.py flask db init`
- `FLASK_APP=app.py flask db migrate -m "creation of all tables"`
- `FLASK_APP=app.py flask db upgrade`

## Run the project

`FLASK_APP=app.py flask run`

Open the following page : `http://localhost:5000`


