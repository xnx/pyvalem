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
.. _PyPI: https://pypi.org/project/pyvalem/
The PyValem package can be installed either from PyPI_ using pip::

    python3 -m pip install pyvalem

or from the source by running (one of the two) from the project source directory::

    # either
    python setup.py install

    # or
    python3 -m pip install .



For Developers:
===============
To de added.



Examples:
=========

Formula
-------
The basic (state-less) chemical formulas are represented by the ``Formula`` class.
A ``Formula`` object is instantiated from a valid formula string and supports ions,
isotopologues, as well as a few special species. The object contains attributes with
its HTML and LaTeX representations, and its molar mass::

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
"Stateful" species are formulas which consist of a valid ``Formula`` string,
followed by whitespace, followed by a semicolon-delimited sequence of valid
quantum state or label specifications. Stateful species know which states they possess and can render these states in different ways. For example::

    In [18]: from pyvalem.stateful_species import StatefulSpecies
    In [19]: ss1 = StatefulSpecies('Ne+ 1s2.2s2.2p5; 2P_1/2')
    In [20]: ss1.states
    Out[21]: [1s2.2s2.2p5, 2P_1/2]

    In [22]: ss1.states[1].__class__
    Out[22]: pyvalem.atomic_term_symbol.AtomicTermSymbol

    In [23]: ss1.html
    Out[23]: 'Ne<sup>+</sup> 1s<sup>2</sup>2s<sup>2</sup>2p<sup>5</sup>; <sup>2</sup>P<sub>1/2</sub>'

This HTML renders as:

.. raw:: html

    Ne<sup>+</sup> 1s<sup>2</sup>2s<sup>2</sup>2p<sup>5</sup>; <sup>2</sup>P<sub>1/2</sub>

.. raw:: latex

    $\mathrm{Ne}^+ \; 1s^22s^22p^5; \; {}^2P_{1/2}$

Another example::

    In [24]: ss2 = StatefulSpecies('(52Cr)(1H) 1σ2.2σ1.1δ2.1π2; 6Σ+; v=0; J=2')
    In [25]: ss2.html
    <sup>52</sup>Cr<sup>1</sup>H 1σ<sup>2</sup>.2σ<sup>1</sup>.1δ<sup>2</sup>.1π<sup>2</sup>; <sup>6</sup>Σ<sup>+</sup>; v=0; J=2

which produces:

.. raw:: html

    <sup>52</sup>Cr<sup>1</sup>H 1σ<sup>2</sup>.2σ<sup>1</sup>.1δ<sup>2</sup>.1π<sup>2</sup>; <sup>6</sup>Σ<sup>+</sup>; v=0; J=2

.. raw:: latex

    $\mathrm{{}^{52}Cr^1H} \; 1\sigma^2.2\sigma^1.1\delta^2.1\pi^2; \; {}^6\Sigma^+; \; v=0; \; J=2$

The syntax for writing different types of quantum state are described in later pages of this documentation.


Reaction
--------
To be added.