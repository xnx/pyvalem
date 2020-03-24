Reaction
********

A ``Reaction`` object is a collection of reactants and a collection of products, each of which is represented by a ``StatefulSpecies`` (though an individual species need not be associated with a specified state). It is instantiated using a string consisting of reactant and product ``StatefulSpecies``, each separated by a plus sign surrounded by whitespace: ``' + '``. Reactants and products are separated by any of the following strings: ``' → '``, ``' = '``, ``' ⇌ '``, ``' -> '``, ``' <-> '``, ``' <=> '``. Examples::

    In [1]: from pyvalem.reaction import Reaction
    In [2]: r1 = Reaction('CO + O2 → CO2 + O')
    In [3]: r2 = Reaction('CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O')
    In [4]: r3 = Reaction('HCl + hv -> H+ + Cl + e-')
    In [5]: r4 = Reaction('C6H5OH + 7O2 → 6CO2 + 3H2O')

An HTML representation of the reaction is returned by the ``html`` attribute::

    In [6] print(r2.html)
    CO v=1 + O<sub>2</sub> J=2; X(<sup>3</sup>Σ<sup>-</sup><sub>g</sub>) → CO<sub>2</sub> + O
    In [7] print(r4.html)
    C<sub>6</sub>H<sub>5</sub>OH + 7O<sub>2</sub> → 6CO<sub>2</sub> + 3H<sub>2</sub>O

These examples render as:

.. raw:: html

    CO v=1 + O<sub>2</sub> J=2; X(<sup>3</sup>Σ<sup>-</sup><sub>g</sub>) → CO<sub>2</sub> + O

.. raw:: latex

    $\mathrm{C}\mathrm{O} \; v=1 + \mathrm{O}_{2} \; J=2; \; X({}^{3}\Sigma^-_{g}) \rightarrow \mathrm{C}\mathrm{O}_{2} + \mathrm{O}$\\
    $\mathrm{C}_{6}\mathrm{H}_{5}\mathrm{O}\mathrm{H} + 7\mathrm{O}_{2} \rightarrow 6\mathrm{C}\mathrm{O}_{2} + 3\mathrm{H}_{2}\mathrm{O}$

``Reaction`` objects are validated to ensure that the charge and stoichiometry are conserved::

    In [8]: Reaction('BeH+ + I2 ⇌ BeI + HI')
    ...
    ReactionChargeError: Charge not preserved for reaction: BeH+ + I2 ⇌ BeI + HI

    In [9]: Reaction('BeH + I2 ⇌ BeI')
    ...
    ReactionStoichiometryError: Stoichiometry not preserved for reaction: BeH + I2 ⇌ BeI
