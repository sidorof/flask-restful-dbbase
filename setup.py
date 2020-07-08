#! /usr/bin/env python
#
# Copyright (c) 2020 Donald Smiley <dsmiley@sidorof.com>
# License: MIT
from setuptools import setup, find_packages

PACKAGE_NAME = "Flask-RESTful-DBBase"
DESCRIPTION = (
    "A package that extends Flask-RESTful resources to "
    "make creating resources for database use easier and faster."
)
with open("README.md") as fobj:
    LONG_DESCRIPTION = fobj.read()

PROJECT_URL = "https://sidorof.github.io/flask-restful-dbbase/"
LICENSE = "MIT"
AUTHOR = "Donald Smiley"
AUTHOR_EMAIL = "dsmiley@sidorof.com"
PYTHON_REQUIRES = ">=3.6"
ZIP_SAFE = False
INSTALL_REQUIRES = [
    "flask",
    "Flask-RESTful",
    "Flask-SQLAlchemy",
    "DBBase",
    "python-dateutil",
    "inflect",
]
EXTRAS_REQUIRE = {"dev": ["unittest", "pytest"]}
CLASSIFIERS = [
    "Framework :: Flask",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

__version__ = None
exec(open("flask_restful_dbbase/_version.py", encoding="utf-8").read())

setup(
    name=PACKAGE_NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=PROJECT_URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    zip_safe=ZIP_SAFE,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    classifiers=CLASSIFIERS,
    packages=find_packages(
        exclude=(
            [
                "*.tests",
                "*.tests.*",
                "tests.*",
                "tests",
                "tests",
                "docs",
                "docsrc",
            ]
        )
    ),
)
