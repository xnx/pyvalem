PyValem
*******

PyValem is a Python package for parsing, validating and interpreting the
chemical formulas, quantum states, species and reactions of atoms, ions and
small molecules, written in a plain-text notation such as ``Na 3p 2Po_3/2``,
``CO X(1Σ+) v=1 J=2`` or ``e- + CO2 -> CO + O-``.

The notation is specified independently of Python in `spec/notation.md`_, with
test vectors that any implementation of it can be checked against. PyValem's
source code is on GitHub_, and it is installed from PyPI_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction.rst
   formula.rst
   states.rst
   stateful_species.rst
   reaction.rst
   examples.rst

.. _spec/notation.md: https://github.com/xnx/pyvalem/blob/main/spec/notation.md
.. _GitHub: https://github.com/xnx/pyvalem
.. _PyPI: https://pypi.org/project/pyvalem/
