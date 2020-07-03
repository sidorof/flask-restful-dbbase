cd ../ && \
	rm -rf ../docs/* && \
	rm -rf build && \
	rm -rf dist && \
	rm -rf flask_restful_dbbase.egg-info 	&& \
	python setup.py install -f && \
	python setup.py sdist bdist_wheel && \
	cd - && \
	rm -rf source/_generated && \
	rm -rf build/* && \
	python owner_app_v1_code.py && \
	python owner_app_v2_code.py && \
	make html && \
	make github
	touch ../docs/.nojekyll


