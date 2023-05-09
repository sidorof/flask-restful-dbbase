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
    python examples/simple_app.py &
    python examples/invoice_app.py &
    python examples/post_only_resource.py &
    python examples/owner_app_v1.py &
    python examples/owner_app_v2.py &

    python simple_app_code.py && \
    python owner_app_v1_code.py && \
    python owner_app_v2_code.py && \
    python invoice_app_code.py && \
    python post_only_resource_code.py \
    make html && \
    make github
    touch ../docs/.nojekyll


