# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
from pathlib import Path

# -- Project information -----------------------------------------------------

project = "PyValem"
copyright = "2022, Christian Hill"
author = "Christian Hill"

# The full version, including alpha/beta/rc tags, read from the package so that
# the documentation doesn't need it to be installed.
_init = Path(__file__).parents[2] / "src" / "pyvalem" / "__init__.py"
release = re.search(r'^__version__ = "(.+)"', _init.read_text(), re.M).group(1)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

latex_engine = "xelatex"
