Formula
*******

A ``Formula`` object instance represents the chemical formula of an atom, isotope, ion,
molecule, molecular ion, or certain sorts of other particle.
The ``Formula`` class has methods for producing representations of the formula in HTML,
LaTeX and plain text.

``Formula`` objects are not supposed to be unique (different ``Formula`` objects can
represent the same formula); nor is their syntax or this library designed to be applied
to large or complex molecules.
PyValem is intended as a lightweight, easy-to-use library with an expressive syntax
for representing many common small atoms and molecules and their isotopes,
states and reactions.

Furthermore, whilst some validation functionality is built into the library,
PyValem does not attempt to verify that a provided formula is chemically plausible.
In particular, it knows nothing about valence or oxidation state.


Instantiation
=============

A ``Formula`` object may be instantiated by passing a valid string, conforming to the
following grammar:

* Single atoms, with atomic weights given by a default natural isotopic abundance are
  specified with their element symbol, e.g. ``H``, ``Be``, ``Fr``.
* Isotopes are specified in parentheses (round brackets) with the isotope mass number
  preceding the element symbol, e.g. ``(12C)``, ``(35Cl)``, ``(235U)``.
  Note that no caret (``^``) is used to indicate a superscript.
* Charged species are specified with the charge following the formula in the format
  ``+n`` or ``-n``, where ``n`` may be omitted if it is 1.
  Do not use a caret (``^``) to indicate a superscript.
  For example, ``He+``, ``C+2``, ``W-``, ``(79Br)-2``.
* Molecular formulas are written as a sequence of element symbols (which may be
  repeated for clarity over the structure), with their stoichiometries specified as
  an integer following the symbol. No underscore (``_``) character is used.
  For example, ``H2O``, ``(1H)2(16O)``, ``C2H6OH``, ``CH3CH2OH``, ``NH+``, ``CO3+2``.
* Moieties within formula can be bracketed for clarity, for example ``CH3C(CH3)2CH3``.
* A limited number of formula prefixes are supported, for example ``L-CH3CH(NH2)CO2H``,
  ``cis-CH3CHCHCH3``, ``ortho-C6H4(CH3)2``
* There are some special species:
    * ``e-`` is the electron;
    * ``e+`` is the positron;
    * ``M`` is a generic third-body with no specific identity (and no defined mass or
      charge);
    * ``hν`` (or ``hv``) is the photon.


Output as HTML, LaTeX and slugs
===============================

The ``Formula`` attributes ``html`` and ``latex`` return strings representing the
formula in HTML and LaTeX respectively.
The attribute ``slug`` returns a URL-safe slug which uniquely identifies the
formula's plain text string. For example:

.. code-block:: pycon

    >>> from pyvalem.formula import Formula
    >>> f = Formula("Co(H2O)6+2")
    >>> print(f.formula)  # or simply print(f)
    Co(H2O)6+2

    >>> print(f.html)
    Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>

    >>> print(f.latex)
    \mathrm{Co}(\mathrm{H}_{2}\mathrm{O})_{6}^{2+}

    >>> print(f.slug)
    Co-_l_H2O_r_6_p2

The HTML and LaTeX representations render as:

.. raw:: html

    Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>

.. raw:: latex

    $\mathrm{Co}(\mathrm{H}_{2}\mathrm{O})_{6}^{2+}$


Formula Attributes
==================

``Formula`` objects can count atoms, calculate masses, record the total species charge,
etc:

.. code-block:: pycon

    >>> f = Formula('CO3-2')
    >>> f.natoms
    4

    >>> round(f.rmm, 3)  # relative molecular mass
    60.008

    >>> f.charge
    -2

    >>> dict(f.atom_stoich)
    {'C': 1, 'O': 3}

    >>> lys = Formula('(NH3+)(CH2)4CH(NH2)CO2-')
    >>> lys.natoms
    24

    >>> round(lys.rmm, 2)
    146.19

    >>> lys.charge
    0

This last example is the Lysine zwitterion,

.. raw:: html

    (NH<sub>3</sub><sup>+</sup>)(CH<sub>2</sub>)<sub>4</sub>CH(NH<sub>2</sub>)CO<sub>2</sub><sup>-</sup>

.. raw:: latex

    $(\mathrm{N}\mathrm{H}_{3}^{+})(\mathrm{C}\mathrm{H}_{2})_{4}\mathrm{C}\mathrm{H}(\mathrm{N}\mathrm{H}_{2})\mathrm{C}\mathrm{O}_{2}^{-}$

The same applies to isotopes and isotopically-pure molecules, in which case the exact
mass is held by the ``mass`` attribute:

.. code-block:: pycon

    >>> f = Formula('(1H)(35Cl)+')
    >>> f.mass
    35.9766777262

The stoichiometric formula can be output either in order of increasing atomic number
(the default) or in alphabetical order:

.. code-block:: pycon

    >>> lys.stoichiometric_formula()
    'H14C6N2O2'

    >>> lys.stoichiometric_formula('alphabetical')
    'C6H14N2O2'
