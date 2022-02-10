|Tests action| |GitHub license| |PyPI version| |PyPI pyversions| |Code style|

.. |Tests action| image:: https://github.com/xnx/pyvalem/workflows/tests/badge.svg
   :target: https://github.com/xnx/pyvalem/actions
.. |GitHub license| image:: https://img.shields.io/github/license/xnx/pyvalem.svg
   :target: https://github.com/xnx/pyvalem/blob/master/LICENSE
.. |PyPI version| image:: https://img.shields.io/pypi/v/pyvalem.svg
   :target: https://pypi.python.org/pypi/pyvalem/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pyvalem.svg
   :target: https://pypi.python.org/pypi/pyvalem/
.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

***********************
Introduction to PyValem
***********************



PyValem is a Python package for parsing, validating, manipulating and
interpreting the chemical formulas, quantum states and labels of atoms, ions
and small molecules.

Species and states are specified as strings using a simple and flexible syntax,
and may be compared, output in different formats and manipulated using a
variety of predefined Python methods.



Installation:
=============

The PyValem package can be installed either from PyPI_ using pip

.. code-block:: bash

    python3 -m pip install pyvalem

or from the source by running (one of the two) from the project source directory.

.. code-block:: bash

    # either
    python setup.py install

    # or
    python3 -m pip install .



Examples:
=========

Formula
-------
The basic (state-less) chemical formulas are represented by the ``Formula`` class.
A ``Formula`` object is instantiated from a valid formula string and supports ions,
isotopologues, as well as a few special species.
The object contains attributes with its HTML and LaTeX representations,
and its molar mass.

.. code-block:: pycon

    >>> from pyvalem.formula import Formula

    >>> # neutral formulas:
    >>> Formula('C2H5OH')
    C2H5OH

    >>> # isotopes:
    >>> Formula('(14C)')
    (14C)

    >>> # ions
    >>> [Formula('H3O+'), Formula('(1H)(2H)+'), Formula('Co(H2O)6+2')]
    [H3O+, (1H)(2H)+, Co(H2O)6+2]

    >>> # special species
    >>> [Formula('e-'), Formula('hv')]
    [e-, hν]

    >>> # formula attributes:
    >>> Formula('Ar+2').charge
    2

    >>> Formula('H2(18O)').html
    'H<sub>2</sub><sup>18</sup>O'

    >>> print(Formula('H2(18O)').latex)
    \mathrm{H}_{2}^{18}\mathrm{O}

    >>> Formula('(235U)').mass
    235.04392819


"Stateful" Species
------------------
The "stateful" species represent species with (or without) any number of states
attached.
The ``StatefulSpecies`` object can be instantiated from a valid string, which consist
of a valid ``Formula`` string, followed by a whitespace, followed by a
semicolon-delimited sequence of valid ``State`` strings.
PyValem supports several different types of state notation.
For further information on valid PyValem ``State`` strings, consult the documentation.

Examples:

.. code-block:: pycon

    >>> from pyvalem.stateful_species import StatefulSpecies

    >>> stateful_species = StatefulSpecies('Ne+ 1s2.2s2.2p5; 2P_1/2')
    >>> stateful_species.formula
    Ne+

    >>> type(stateful_species.formula)
    <class 'pyvalem.formula.Formula'>

    >>> stateful_species.states
    [1s2.2s2.2p5, 2P_1/2]

    >>> state1, state2 = stateful_species.states
    >>> type(state1)
    <class 'pyvalem.states.atomic_configuration.AtomicConfiguration'>

    >>> state1.orbitals
    [1s2, 2s2, 2p5]

    >>> type(state2)
    <class 'pyvalem.states.atomic_term_symbol.AtomicTermSymbol'>

    >>> state2.L, state2.J
    (1, 0.5)

As ``Formula``, also ``StatefulSpecies`` have ``html`` and ``latex`` attributes.

.. code-block:: pycon

    >>> print(stateful_species.latex)
    \mathrm{Ne}^{+} \; 1s^{2}2s^{2}2p^{5}; \; {}^{2}P_{1/2}

    >>> StatefulSpecies('(52Cr)(1H) 1sigma2.2sigma1.1delta2.1pi2; 6SIGMA+; v=0; J=2').html
    '<sup>52</sup>Cr<sup>1</sup>H 1σ<sup>2</sup>.2σ<sup>1</sup>.1δ<sup>2</sup>.1π<sup>2</sup> <sup>6</sup>Σ<sup>+</sup> v=0 J=2'


Reaction
--------
Finally, the ``Reaction`` class represents a reaction or a collisional process between
species. A ``Reaction`` object is instantiated with a string consisting of valid
``Formula`` or ``StatefulSpecies`` strings delimited by ``' + '``, and reaction sides
separated by ``' -> '``, such as

.. code-block:: pycon

    >>> from pyvalem.reaction import Reaction
    >>> reaction = Reaction('He+2 + H -> He+ 3p1 + H+ + hv')
    >>> reaction
    He+2 + H → He+ 3p + H+ + hν

    >>> reaction.html
    'He<sup>2+</sup> + H → He<sup>+</sup> 3p + H<sup>+</sup> + hν'

    >>> print(reaction.latex)
    \mathrm{He}^{2+} + \mathrm{H} \rightarrow \mathrm{He}^{+} \; 3p + \mathrm{H}^{+} + h\nu

The ``Reaction`` class also watches out for charge balance and stoichiometry
conservation during instantiation.

.. code-block:: pycon

    >>> Reaction('(2H) + (3H) -> (4He)')
    Traceback (most recent call last):
    ...
    pyvalem.reaction.ReactionStoichiometryError: Stoichiometry not preserved for reaction: (2H) + (3H) -> (4He)

    >>> Reaction('e- + Ar -> Ar+ + e-')
    Traceback (most recent call last):
    ...
    pyvalem.reaction.ReactionChargeError: Charge not preserved for reaction: e- + Ar -> Ar+ + e-



For Developers:
===============
It goes without saying that any development should be done in a clean virtual
environment.
After cloning or forking the project from its GitHub_ page, ``pyvalem`` might be
installed into the virtual environment in editable mode with

.. code-block:: bash

    pip install -e .[dev]

The ``[dev]`` extra installs (apart from the package dependencies) also several
development-related packages, such as ``pytest``, ``black``, ``tox`` or ``ipython.``
The tests can then be executed by running (from the project root directory)

.. code-block:: bash

    # either
    pytest

    # or
    tox

The project does not have ``requirements.txt`` by design, all the package dependencies
are rather handled by ``setup.py``.
The package needs to be installed to run the tests, which grants the testing process
another layer of usefulness.

Docstrings in the project adhere to the numpydoc_ styling.
The project code is formatted by ``black``.
Always make sure to format your code before submitting a pull request, by running
``black`` on all your python files.


.. _GitHub: https://github.com/xnx/pyvalem
.. _PyPI: https://pypi.org/project/pyvalem/
.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/format.html
