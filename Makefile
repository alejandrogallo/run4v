dev-install-local:
	python setup.py develop --user
test:
	python setup.py test
install-local:
	python setup.py install --user

doc-html:
	make -C doc/ html

update-gh-pages:
	@echo "Warning: Black magic in action"
	git push origin `git subtree split --prefix doc/build/html/ master`:gh-pages --force
