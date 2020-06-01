cd ../ && \
	rm -rf build && \
	rm -rf dist && \
	rm -rf dbbase.egg-info 	&& \
	python setup.py install -f && \
	python setup.py sdist bdist_wheel && \
	cd - && \
	rm -rf src/_generated && \
	rm -rf build/* && \
	make html && \
	make github 

