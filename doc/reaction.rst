Reaction
********

A ``Reaction`` object is a collection of reactants and a collection of products,
each of which is represented by a ``StatefulSpecies`` (though an individual species
need not be associated with a specified state).
It is instantiated using a string consisting of reactant and product
``StatefulSpecies``, each separated by a plus sign surrounded by whitespace: ``' + '``.
Reactants and products are separated by any of the following strings:
``' → '``, ``' = '``, ``' ⇌ '``, ``' -> '``, ``' <-> '``, ``' <=> '``.

Examples
========

.. code-block:: pycon

    >>> from pyvalem.reaction import Reaction
    >>> r1 = Reaction('CO + O2 → CO2 + O')
    >>> r2 = Reaction('CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O')
    >>> r3 = Reaction('HCl + hv -> H+ + Cl + e-')
    >>> r4 = Reaction('C6H5OH + 7O2 → 6CO2 + 3H2O')

An HTML representation of the reaction is stored as the ``html`` attribute::

    >>> print(r2.html)
    CO v=1 + O<sub>2</sub> J=2; X<sup>3</sup>Σ<sup>-</sup><sub>g</sub> → CO<sub>2</sub> + O
    >>> print(r4.html)
    C<sub>6</sub>H<sub>5</sub>OH + 7O<sub>2</sub> → 6CO<sub>2</sub> + 3H<sub>2</sub>O

These examples render as:

.. raw:: html

    CO v=1 + O<sub>2</sub> J=2; X<sup>3</sup>Σ<sup>-</sup><sub>g</sub> → CO<sub>2</sub> + O
    C<sub>6</sub>H<sub>5</sub>OH + 7O<sub>2</sub> → 6CO<sub>2</sub> + 3H<sub>2</sub>O

The ``Reaction`` objects are validated to ensure that the charge and stoichiometry are
conserved:

.. code-block:: pycon

    >>> Reaction('BeH+ + I2 ⇌ BeI + HI')
    Traceback (most recent call last):
      ...
    pyvalem.reaction.ReactionChargeError: Charge not preserved for reaction: BeH+ + I2 ⇌ BeI + HI

    >>> Reaction('BeH + I2 ⇌ BeI')
    Traceback (most recent call last):
      ...
    pyvalem.reaction.ReactionStoichiometryError: Stoichiometry not preserved for reaction: BeH + I2 ⇌ BeI
