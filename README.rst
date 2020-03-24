Introduction to PyValem
***********************

PyValem is a Python package for parsing, validating, manipulating and
interpreting the chemical formulas, quantum states and labels of atoms, ions
and small molecules.

Species and states are specfied as strings using a simple and flexible syntax,
and may be compared, output in different formats and manipulated using a
variety of predefined Python methods.

Installation
============

From this source::

    python setup.py install

Or using pip::

    pip install pyvalem

Examples
========

The basic (state-less) chemical formula class is ``Formula``. A ``Formula`` object
can be created by passing its constructor a valid string. This object contains
attributes for producing its plain text, HTML and LaTeX representations, and
for calculating its molar mass::

    In [1]: from pyvalem.formula import Formula

    In [2]: f = Formula('C2H5OH')

    In [3]: print(f)
    C2H5OH

    In [4]: print(f.html)
    C<sub>2</sub>H<sub>5</sub>OH

    In [5]: print(f.latex)
    $\mathrm{C}_{2}\mathrm{H}_{5}\mathrm{O}\mathrm{H}$

    In [6]: print(f.rmm)    # g.mol-1
    46.069

Note that there is no underscore character (``_``) before between the element
symbol and its stoichiometry. Isotopes are specified with the mass number
placed before the element symbol, with both surrounded by parentheses. Do not
use a caret (``^``) to indicate a superscript::

    In [7]: f = Formula('(14C)')

    In [8]: print(f.html)
    <sup>14</sup>C

    In [9]: print(f.rmm)
    14.0032419884

    In [10]: f = Formula('H2(18O)')

    In [11]: print(f.rmm)
    20.015159612799998

For isotopically-pure compounds, the mass returned is the atomic mass.

Charges are specified as ``+n`` or ``-n``, where ``n`` may be omitted if it is 1.
Do not use a caret (``^``) to indicate a superscript::

    In [12]: f = Formula('H3O+')
    In [13]: print(f.charge)
    1

    In [14]: print(f.html)
    H<sub>3</sub>O<sup>+</sup>

    In [15]: f = Formula('Co(H2O)6+2')
    In [16]: print(f.charge)
    2

    In [17]: print(f.html)
    Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>

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

