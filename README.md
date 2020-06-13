# Python todos

### Requirements

Python 3 (developed on python 3.8.1)
PostgreSQL

### Installation


python3 -c venv venv
source venv/bin/activate
pip install

### Development

Add .env file with following variables
FLASK_ENV=development
FLASK_APP=index.py
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME

Execute command:
flask run

### License

MIT
