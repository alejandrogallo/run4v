clean: 
	rm ./**/*.pyc
	rm *.pyc

test: 
	python -m unittest discover -v tests
