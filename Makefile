.PHONY: init test clean all install uninstall

init:
	python setup.py build

test:
	python -m unittest tests

clean:
	rm -rf build/

all:
	#pip install -r requirements.txt
	python setup.py build

install:
	#pip install -r requirements.txt
	pip install .

uninstall:
	pip uninstall htopy
