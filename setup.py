from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'pyvalem',
    version = '2.0',
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
        "Intended Audience :: Science/Research"
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    package_data={'pyvalem': ['atomic_weights.txt', 'isotope_masses.txt']},
)


