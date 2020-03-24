Stateful Species
****************

A *stateful species* is a species identified by a chemical formula which is associated with one or more quantum states of labels, and can be represented by an instance of the ``StatefulSpecies`` class.

A ``StatefulSpecies`` object can be instantiated by providing a string consisting of the formula (which can be parsed into a ``Formula`` object), followed by whitespace and a semicolon delimited sequence of strings that can be parsed by one of the ``State`` classes described previously. The state type is deduced from the format of the string.

Examples::

    In [1]: from pyvalem.stateful_species import StatefulSpecies
    In [2]: ss1 = StatefulSpecies('HCl v=2;J=0')
    In [3]: ss2 = StatefulSpecies('NCO v2+3v1;J=10.5;a(2Σ-g)')
    In [4]: ss3 = StatefulSpecies('Ar+ 1s2.2s2.2p5; 2P_3/2')
    In [5]: ss4 = StatefulSpecies('CrH 1sigma2.2sigma1.1pi4.3sigma1; 6SIGMA+')

An HTML representation is accessible through the ``html`` attribute::

    In [6]: print(ss4.html)
    CrH 1σ<sup>2</sup>.2σ<sup>1</sup>.1π<sup>4</sup>.3σ<sup>1</sup>; <sup>6</sup>Σ<sup>+</sup>

This example renders as:

.. raw:: html

    CrH 1σ<sup>2</sup>.2σ<sup>1</sup>.1π<sup>4</sup>.3σ<sup>1</sup>; <sup>6</sup>Σ<sup>+</sup>

.. raw:: latex

    $\mathrm{Cr}\mathrm{H} \; 1\sigma^{2}2\sigma^{1}1\pi^{4}3\sigma^{1}; \; {}^{6}\Sigma^+$

The ``Formula`` object and a list of the parse ``State`` objects are returned by the ``formula`` and ``states`` attributes::

    In [7]: print(ss4.formula)
    CrH

    In [8]: print(ss4.states)
    [1σ2.2σ1.1π4.3σ1, 6Σ+]

Two ``StatefulSpecies`` are considered the same (equal) if they have equal ``Formula`` objects and matching states::

    In [9]: ss5 = StatefulSpecies('CO2 v2+3v1; J=2')
    In [10]: ss6 = StatefulSpecies('CO2 J=2; ν2+3ν1')
    In [11]: ss5 == ss6
    Out[11]: True

Some ``State`` types cannot be repeated within a ``StatefulSpecies`` object (e.g. it doesn't make sense for a molecule to have two rotational quantum numbers, J). This is checked for::

    In [12]: StatefulSpecies('N2 J=0;J=1')
    ...
    StatefulSpeciesError: Multiple states of type RotationalState specified for N2 J=0;J=1

    In [13]: StatefulSpecies('Li 1s2.2s1; 1s2.2p1')
    ...
    StatefulSpeciesError: Multiple states of type AtomicConfiguration specified for Li 1s2.2s1;1s2.2p1
