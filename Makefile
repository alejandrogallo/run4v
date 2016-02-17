dev-install-local:
	python setup.py develop --user
test:
	python setup.py test
install-local:
	python setup.py install --user

doc-html:
	make -C doc/ html
