.PHONY: init test clean all docs install uninstall

init:
	python setup.py build

test:
	python -m unittest tests

clean:
	rm -rf build/

all:
	#pip install -r requirements.txt
	python setup.py build

docs:
	sphinx-apidoc -o docs htopy

install:
	#pip install -r requirements.txt
	pip install .

uninstall:
	pip uninstall htopy
