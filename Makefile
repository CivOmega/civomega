
all: run

install:
	echo "Ensure you're in a virtualenv!"
	pip install -r requirements.txt
	python setup.py develop

run:
	python dataomega/web.py

test:
	nosetests
