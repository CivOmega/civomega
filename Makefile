
all: run

install:
	echo "Ensure you're in a virtualenv!"
	pip install -r requirements.txt
	python setup.py develop

run:
	gunicorn civomega.web:app

test:
	nosetests
