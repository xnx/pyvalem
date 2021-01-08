from setuptools import setup, find_packages

long_description = """PyValem is a Python package for parsing, validating, manipulating and interpreting the chemical formulas, quantum states and labels of atoms, ions and small molecules.

Species and states are specfied as strings using a simple and flexible syntax, and may be compared, output in different formats and manipulated using a variety of predefined Python methods.

See https://github.com/xnx/pyvalem for documentation and more information.
"""

setup(
    name = 'pyvalem',
    version = '2.1.0',
    author = 'Christian Hill',
    author_email = 'ch.hill@iaea.org',
    description = 'A package for managing simple chemical species and states',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/xnx/pyvalem',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.4',
    package_data={'pyvalem': ['atomic_weights.txt', 'isotope_masses.txt']},
)
