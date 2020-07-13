import os
import sys
from datetime import date
import flask_restful_dbbase

sys.path.append('../../examples')
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

project = 'Flask-RESTful-DBBase'
copyright = f'{date.today().year}, Don Smiley'
author = 'Don Smiley'
release = flask_restful_dbbase.__version__
pygments_style = "default"
highlight_language = "python3"

extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.viewcode',
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx_automodapi.automodapi",
    "m2r",
    "flask_sphinx_themes",
    # "pallets_sphinx_themes",
    'sphinxcontrib.fulltoc',
]

templates_path = ['_templates']
exclude_patterns = []

# HTML
html_theme = 'flask'
html_theme_path = ['_themes']

html_static_path = ['_static']

html_theme_options = {
     'index_logo': 'flask-restful-dbbase.svg'
}

html_sidebars = {

    'index': [
        'sidebarintro.html',
        'searchbox.html', 'sourcelink.html'],
     '**': [
         'sidebarlogo.html', 'localtoc.html',
         'relations.html', 'sourcelink.html',
         'searchbox.html'
    ]
}

html_use_modindex = True
html_show_sphinx = False

# -- Options for autodoc -----------------------------------------------------

autoclass_content = "class"
autodoc_typehints = "none"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": False
}

# -- Options for autosummary -----------------------------------------------------

autosummary_generate = True
autosummary_generate_overwrite = True


# -- Options for napoleon--- -----------------------------------------------------

napoleon_use_rtype = False
