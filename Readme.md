# Web App Demo

This is just a small Flask project used to demonstrate the basics of web app hacking. It is intentionally vulnerable in
several ways.

## Usage
To use the application, first install the requirements, and then run the `app/main.py` file. To initialize the database with a user, use the commands in `manage.py`. Here is a quick start with `virtualenv`:

```bash
git clone https://github.com/terrabitz/FlaskWebAppHackingDemo
cd FlaskWebAppHackingDemo
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 manage.py db upgrade
python3 manage.py create_user

python3 app/main.py
```
