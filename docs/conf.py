# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import json

from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
from utils.utils import markdown_to_text

# -- Project information -----------------------------------------------------

project = 'Informatics playbook'
copyright = '2020, CD2H Data Working Group'
author = 'CD2H Data Working Group'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinxext.adaptive_youtube',
    # 'sphinxjp.themes.basicstrap',
    'basicstrap',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'contents'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_additional_pages = {'index': 'index.html', 'about': 'about.html'}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {
    "**": ["globaltoc.html"]
}

# Chapter preview gathering is done here
# We read the md files from the /chapters folder
# Then we read each file separately and convert the files to text after we do some formatting
# and pass the data to the html_context

directory = 'chapters'
preview_dict = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".md"):
        with open(os.path.join(directory, filename), 'r', encoding="utf8") as _file:
            lines = _file.readlines()
            title = ''
            doc = ''
            found_first_line = False
            for index, line in enumerate(lines):
                if not found_first_line:
                    if line.strip():
                        found_first_line = True
                        title = line.replace('#', '').replace('*', '').replace('=', '').replace('\n', '').strip()
                # Ignore headings
                if line.startswith('#') or line.startswith('##') or line.startswith('###'):
                    pass
                else:
                    # We add the space at the end so two lines are not stuck together when
                    # they are joined
                    doc = doc + line + ' '

            # We only need plain text on the preview without any formatting so we do some
            # sanitizing here
            data = doc.replace('\n', '').replace('*', '').replace('=', '').replace('\n', '').strip()
            preview = {
                'document_url': os.path.join(directory, filename).replace('.md', '').replace('\\', '/') + '.html',
                'document_name': os.path.join(directory, filename),
                'document_title': title,
                'preview': markdown_to_text(data)
            }
            preview_dict.append(preview)
        continue
    else:
        continue


def get_static_type(filename):
    if filename.endswith(".css"):
        filetype = 'css'
    elif filename.endswith(".js"):
        filetype = 'js'
    else:
        filetype = 'img'
    return filetype


# get all vue static files to later include them in the layout.html
directory = '../basicstrap/templates/basicstrap/static/vue'
vue_static = []
for item in os.listdir(directory):
    if os.path.isfile(directory + '/' + item):
        filename = '_static/vue/' + item
        vue_static.append({'type': get_static_type(filename), 'path': filename})
    else:
        for innerFile in os.listdir(directory + '/' + item):
            filename = '_static/vue/' + item + '/' + innerFile
            vue_static.append({'type': get_static_type(filename), 'path': filename})

html_context = {
    'author': author,
    'date': datetime.date.today().strftime('%d/%m/%y'),
    'document_previews': preview_dict,
    'document_previews_json': json.dumps(preview_dict),
    'vue_static': vue_static
}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'ReusableDataBestPracticesdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'ReusableDataBestPractices.tex', 'Informatics playbook Documentation',
     'CD2H Data Working Group', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'reusabledatabestpractices', 'Informatics playbook Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'ReusableDataBestPractices', 'Informatics playbook Documentation',
     author, 'ReusableDataBestPractices', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

try:
    html_theme = 'basicstrap'
    html_css_files = [
    ]
    html_js_files = [
    ]
    html_theme_options = {
        'googlewebfont': True,
        'googlewebfont_url': 'https://fonts.googleapis.com/css?family=Roboto',
        'googlewebfont_style': "font-family: 'Roboto', sans-serif",
    }

except ImportError:
    print('Warning: "basicstrap" is not installed, fall back to default theme.')


# set the level of depth for the sidebar
# for now only depth = 2 and depth = 3 makes sense
depth = 3
def setup(app):
    # app.add_stylesheet('_static/css/custom.css')

    # Enable recommonmark's AutoStructify component
    # Ref: https://recommonmark.readthedocs.io/en/latest/auto_structify.html
    github_doc_root = "https://github.com/data2health/reusable-data-best-practices/tree/master/doc"
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'enable_auto_toc_tree': True,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_math': True,
        'enable_inline_math': True
    }, True)

    app.add_transform(AutoStructify)
