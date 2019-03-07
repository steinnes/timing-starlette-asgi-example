setup:
	virtualenv venv

venv: setup
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python app.py
