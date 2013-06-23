
all: run

install:
	echo "Ensure you're in a virtualenv!"
	pip install -r requirements.txt
	python setup.py develop

run:
	foreman start

test:
	nosetests
