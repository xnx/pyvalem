import os
from setuptools import setup, find_packages

long_description = """PyValem is a Python package for parsing, validating, manipulating and interpreting the chemical formulas, quantum states and labels of atoms, ions and small molecules.

Species and states are specfied as strings using a simple and flexible syntax, and may be compared, output in different formats and manipulated using a variety of predefined Python methods.

See https://github.com/xnx/pyvalem for documentation and more information.
"""

# Read in dependencies list from requirements.txt
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name = 'pyvalem',
    version = '2.3.0',
    author = 'Christian Hill, Martin Hanicinec',
    author_email = 'ch.hill@iaea.org',
    description = 'A package for managing simple chemical species and states',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/xnx/pyvalem',
    packages = find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.4',
    package_data={'pyvalem': ['atomic_weights.txt', 'isotope_masses.txt']},
)
