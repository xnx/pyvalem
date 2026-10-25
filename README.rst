|Tests action| |Docs| |GitHub license| |PyPI version| |PyPI pyversions| |Code style|

.. |Tests action| image:: https://github.com/xnx/pyvalem/workflows/tests/badge.svg
   :target: https://github.com/xnx/pyvalem/actions
.. |Docs| image:: https://readthedocs.org/projects/pyvalem/badge/?version=latest
   :target: https://pyvalem.readthedocs.io/
.. |GitHub license| image:: https://img.shields.io/github/license/xnx/pyvalem.svg
   :target: https://github.com/xnx/pyvalem/blob/main/LICENSE
.. |PyPI version| image:: https://img.shields.io/pypi/v/pyvalem.svg
   :target: https://pypi.python.org/pypi/pyvalem/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pyvalem.svg
   :target: https://pypi.python.org/pypi/pyvalem/
.. |Code style| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff

***********************
Introduction to PyValem
***********************



PyValem is a Python package for parsing, validating, manipulating and
interpreting the chemical formulas, quantum states and labels of atoms, ions
and small molecules.

Species and states are specified as strings using a simple and flexible syntax,
and may be compared, output in different formats and manipulated using a
variety of predefined Python methods.

The documentation is at https://pyvalem.readthedocs.io/.



Installation:
=============

The PyValem package can be installed either from PyPI_ using pip

.. code-block:: bash

    python3 -m pip install pyvalem

or from the source by running the following from the project source directory.

.. code-block:: bash

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
    \mathrm{H}_{2}{}^{18}\mathrm{O}

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
    \mathrm{Ne}^{+} \; 1s^{2}2s^{2}2p^{5} \; {}^{2}\mathrm{P}_{1/2}

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


Errors
------
Every exception that PyValem raises for an invalid formula, state, species or
reaction derives from ``PyValemError``, which is itself a ``ValueError``:

.. code-block:: pycon

    >>> from pyvalem import PyValemError
    >>> try:
    ...     Reaction('H2 v=1.5 + O -> OH + H')
    ... except PyValemError as err:
    ...     print(type(err).__name__)
    VibrationalStateError


More examples
-------------
The `examples`_ directory has short scripts that check a list of reactions before
it goes into a database, and that apply the selection rules for atomic transitions
to levels written in PyValem's notation.

.. _examples: https://github.com/xnx/pyvalem/tree/main/examples


Specification:
==============
The notation that PyValem implements is specified, independently of Python, in
`spec/notation.md`_, with test vectors in `spec/tests`_ that any implementation of
the notation can be checked against.

.. _spec/notation.md: https://github.com/xnx/pyvalem/blob/main/spec/notation.md
.. _spec/tests: https://github.com/xnx/pyvalem/tree/main/spec/tests


For Developers:
===============
After cloning or forking the project from its GitHub_ page, install ``pyvalem`` in
editable mode into a clean virtual environment, together with its development
dependencies (this needs pip 25.1 or later):

.. code-block:: bash

    python3 -m pip install -e . --group dev

The tests can then be executed by running (from the project root directory)

.. code-block:: bash

    pytest

The package metadata and all of its dependencies are declared in ``pyproject.toml``.

Docstrings in the project adhere to the numpydoc_ styling.
The project code is linted and formatted by ruff_ (installed with the ``dev``
group). Before submitting a pull request, run

.. code-block:: bash

    ruff check
    ruff format


.. _GitHub: https://github.com/xnx/pyvalem
.. _PyPI: https://pypi.org/project/pyvalem/
.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/format.html
.. _ruff: https://docs.astral.sh/ruff/
