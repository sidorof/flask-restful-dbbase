cd ../ && \
	rm -rf build && \
	rm -rf dist && \
	rm -rf flask_restful_dbbase.egg-info 	&& \
	python setup.py install -f && \
	python setup.py sdist bdist_wheel && \
	cd - && \
	rm -rf source/_generated && \
	rm -rf build/* && \
	make html && \
	make github

