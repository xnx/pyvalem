States
******

PyValem recognises several different kinds of quantum states and labels and is able to
deduce the state type, parse quantum numbers and symmetries from provided strings,
and do some validation.

States of different types can be instantiated directly from their class or associated
with a species formula as a ``StatefulSpecies`` object.

``GenericExcitedState``
=======================

A "generic excited state" is simply an unspecified excitation of the species above its
ground state: it may represent excitation of a single species to an unspecified quantum
level or the general excitation of an ensemble of such species to a range of levels
under equilibrium or non-equilibrium conditions.

A ``GenericExcitedState`` object is instantiated as a string of 1-4 asterisks or as a
number preceding a single asterisk. For example:

.. code-block:: pycon

    >>> from pyvalem.states import GenericExcitedState
    >>> x0 = GenericExcitedState('*')
    >>> x1 = GenericExcitedState('***')
    >>> x2 = GenericExcitedState('5*')


``AtomicConfiguration``
=======================

The electronic configuration of atoms, ions and isotopes is represented by the
``AtomicConfiguration`` class. The string representation provided to instantiate an
``AtomicConfiguration`` object is a sequence of orbital specifiers, separated by a
full stop (period, ``.``). An atomic orbital is represented by its principal
quantum number, ``n``, the azimuthal quantum number, ``l`` written as the
letter ``s``, ``p``, ``d``, ..., and the an occupancy (number of electrons, ``1`` or
``2``). For example:

.. code-block:: pycon

    >>> from pyvalem.states import AtomicConfiguration
    >>> c0 = AtomicConfiguration('1s2')
    >>> c1 = AtomicConfiguration('1s2.2s2.2p6')
    >>> c2 = AtomicConfiguration('1s2.2s2.2p6.3s2.3d10')

The closed-shell part of an atomic configuration can be specified by providing the
corresponding noble gas element symbol in square brackets:

.. code-block:: pycon

    >>> c2 =  AtomicConfiguration('[Ne].3s2.3d10')

The HTML representation of the atomic configuration is returned by the ``html``
attribute:

.. code-block:: pycon

    >>> print(c2.html)
    [Ne]3s<sup>2</sup>3d<sup>10</sup>

which renders as:

.. raw:: html

    [Ne]3s<sup>2</sup>3d<sup>10</sup>

If the same atomic orbital appears more than once or an orbital is specified as being
occupied by more than the number of electrons allowed by the Pauli exclusion principle,
an ``AtomicConfigurationError`` is raised:

.. code-block:: pycon

    >>> c3 = AtomicConfiguration('[Ar].3s2')
    Traceback (most recent call last):
      ...
    pyvalem.states.atomic_configuration.AtomicConfigurationError: Repeated subshell in [Ar].3s2

    >>> c3 = AtomicConfiguration('1s2.2s2.2p7')
    Traceback (most recent call last):
      ...
    pyvalem.states.atomic_configuration.AtomicConfigurationError: Too many electrons in atomic orbital: 2p7


``AtomicTermSymbol``
====================

The ``AtomicTermSymbol`` class represents an atomic electronic term symbol in the
LS-coupling (Russell–Saunders coupling) notation.
The total electronic spin quantum number, S, is specified by a multiplicity, 2S+1,
followed by the total electronic orbital angular momentum quantum number, L, as a
letter, ``S``, ``P``, ``D``, ... for L = 0, 1, 2, ...; there may optionally follow a
parity label, ``o`` (for odd-parity states), and a total (spin-orbit coupled)
electronic angular momentum quantum number, J after an underscore character (``_``).
Half (odd)-integers are specified as fractions: ``1/2``, ``3/2``, ``5/2``, etc.

Examples:

.. code-block:: pycon

    >>> from pyvalem.states import AtomicTermSymbol
    >>> a0 = AtomicTermSymbol('3P_1')
    >>> a1 = AtomicTermSymbol('4D')
    >>> a2 = AtomicTermSymbol('2Po_1/2')

``AtomicTermSymbol`` objects know about their quantum numbers, where defined:

.. code-block:: pycon

    >>> a0.S, a0.L, a0.J
    (1.0, 1, 1.0)

    >>> a1.S, a1.L, a1.J
    (1.5, 2, None)

    >>> a2.S, a2.L, a2.J, a2.parity
    (0.5, 1, 0.5, 'o')

As with other states, the ``html`` attribute returns the HTML representation:

.. code-block:: pycon

    >>> print(a2.html)
    <sup>2</sup>P<sup>o</sup><sub>1/2</sub>

which renders as:

.. raw:: html

    <sup>2</sup>P<sup>o</sup><sub>1/2</sub>

J must satisfy the "triangle rule" (\|L-S\| ≤ J ≤ L+S); if this test fails, an
``AtomicTermSymbolError`` is raised:

.. code-block:: pycon

    >>> a3 = AtomicTermSymbol('3P_3')
    Traceback (most recent call last):
      ...
    pyvalem.states.atomic_term_symbol.AtomicTermSymbolError: Invalid atomic term symbol: 3P_3 |L-S| <= J <= L+S must be satisfied.

A single, lowercase letter label to distinguish term symbols with the same ``S``, ``L`` that arise from the same atomic configuration; the convention assumed to be followed is that of C. E. Moore, NBS Circ, No. 488 (1950). See e.g. G. Nave et al., Astrophys. J. Suppl. Ser. 94:221-459 (1994). Terms with the same ``S`` and ``L`` of even parity are labelled in order of increasing energy as ``a``, ``b``, etc.; terms with odd parity are labelled in order of increasing energy as ``z``, ``y``, ``x``, etc.

.. code-block:: pycon

    >>> from pyvalem.states import AtomicTermSymbol
    >>> a0 = AtomicTermSymbol('a5D')
    >>> a1 = AtomicTermSymbol('b5D')
    >>> a2 = AtomicTermSymbol('z3Po')
    >>> a3 = AtomicTermSymbol('y3Po')


``DiatomicMolecularConfiguration``
==================================

The electronic configuration of diatomic molecules, molecular ions and their
isotopologues is represented by the ``DiatomicMolecularConfiguration`` class.
This class is instantiated with a string consisting of a sequence of numbered molecular
orbitals, separated by a full stop (period, ``.``).
Each orbital is denoted with a counting number (which increments for each orbital of
the same symmetry), an orbital symmetry label, and an electron occupancy number.

The valid symmetry labels are the lower case greek letters,
``σ``, ``π``, and ``δ``, with an optional letter, ``u`` or ``g`` denoting the inversion
symmetry for centrosymmetric molecules.
For convenience, the identifiers ``sigma``, ``pi``, ``delta`` may be used as
identifiers instead of the greek labels.

Examples:

.. code-block:: pycon

    >>> from pyvalem.states import DiatomicMolecularConfiguration
    >>> c1 = DiatomicMolecularConfiguration('1σ')
    >>> c2 = DiatomicMolecularConfiguration('1σu2')
    >>> c3 = DiatomicMolecularConfiguration('1piu4.1pig3')
    >>> c4 = DiatomicMolecularConfiguration('1σg2.1σu2.2σg2.2σu2.1πu4.3σg2')

An HTML representation of the configuration is held in the ``html`` attribute:

.. code-block:: pycon

    >>> print(c3.html)
    1π<sub>u</sub><sup>4</sup>.1π<sub>g</sub><sup>3</sup>

    >>> print(c4.html)
    1σ<sub>g</sub><sup>2</sup>.1σ<sub>u</sub><sup>2</sup>.2σ<sub>g</sub><sup>2</sup>.2σ<sub>u</sub><sup>2</sup>.1π<sub>u</sub><sup>4</sup>.3σ<sub>g</sub><sup>2</sup>

These render as:

.. raw:: html

    1π<sub>u</sub><sup>4</sup>.1π<sub>g</sub><sup>3</sup>       <br/>
    1σ<sub>g</sub><sup>2</sup>.1σ<sub>u</sub><sup>2</sup>.2σ<sub>g</sub><sup>2</sup>.2σ<sub>u</sub><sup>2</sup>.1π<sub>u</sub><sup>4</sup>.3σ<sub>g</sub><sup>2</sup>


An attempt to fill an orbital with too many electrons raises a
``DiatomicMolecularConfigurationError``, as does repeating an orbital:

.. code-block:: pycon

    >>> c5 = DiatomicMolecularConfiguration('1σ2.2σ2.3σ3')
    Traceback (most recent call last):
      ...
    pyvalem.states.diatomic_molecular_configuration.DiatomicMolecularConfigurationError: Only two electrons allowed in σ orbital, but received 3

    >>> c6 = DiatomicMolecularConfiguration('1σ2.2σ2.2σ1')
    Traceback (most recent call last):
      ...
    pyvalem.states.diatomic_molecular_configuration.DiatomicMolecularConfigurationError: Repeated orbitals in 1σ2.2σ2.2σ1


``MolecularTermSymbol``
=======================

The ``MolecularTermSymbol`` class represents a molecular electronic term symbol.
It is instantiated with a string providing the spin multiplicity (2S+1),
electronic orbital angular momentum symmetry label and (optionally) the quantum
number Ω in the Hund's case (a) formulation.

Symmetry labels are specified as an appropriate letter combination representing the
irreducible representation of the electronic orbital wave function. For molecules with
a centre of symmetry, the ``u``/``g`` label comes last, preceded by any ``+``/``-``
label denoting the reflection symmetry of the wave function. Do not use a caret (``^``)
or underscore (``_``) character to indicate superscripts or subscripts.
For linear molecules, the irrep symbols ``Σ``, ``Π``, ``Δ`` and ``Φ`` may be replaced
with ``SIGMA``, ``PI``, ``DELTA``, and ``PHI``.

If a term symbol has a label, this is given before the term symbol itself, which
should be enclosed with parentheses.

Examples:

.. code-block:: pycon

    >>> from pyvalem.states import MolecularTermSymbol
    >>> c1 = MolecularTermSymbol('1Σ-')
    >>> c2 = MolecularTermSymbol('1SIGMA-')
    >>> c3 = MolecularTermSymbol('3Σ+g')
    >>> c4 = MolecularTermSymbol('3SIGMA+g')
    >>> c5 = MolecularTermSymbol('b(4Π_-3/2)')
    >>> c6 = MolecularTermSymbol("A'(1A1g_0)")
    >>> c7 = MolecularTermSymbol('A(1A")')

The ``html`` attribute returns the HTML representation of the molecular term symbol.
The examples above are represented by:

.. raw:: html

    <sup>1</sup>Σ<sup>-</sup>		<br/>
    <sup>1</sup>Σ<sup>-</sup>		<br/>
    <sup>3</sup>Σ<sup>+</sup><sub>g</sub>		<br/>
    <sup>3</sup>Σ<sup>+</sup><sub>g</sub>		<br/>
    b(<sup>4</sup>Π<sub>-3/2</sub>)		<br/>
    A'(<sup>1</sup>A<sub>1g</sub><sub>0</sub>)		<br/>
    A(<sup>1</sup>A")		<br/>


``MolecularTermSymbol`` objects know about their total spin angular momentum quantum
number, S, the electronic orbital angular momentum wave function irrep, the projection
of the total angular momentum along the symmetry axis, Ω, and the term label.
For example:

.. code-block:: pycon

    >>> c6 = MolecularTermSymbol('X(4Πu_-3/2)')
    >>> c6.S, c6.term_label, c6.irrep, c6.Omega
    (1.5, 'X', 'Πu', -1.5)


``VibrationalState``
====================

Molecular vibrational states of diatomic and polyatomic molecules are represented by
the ``VibrationalState`` class. For diatomic molecules, this class is instantiated
with a string of the form ``v=n`` for ``n=0,1,2,...``. Polyatomic vibrational states
are initialised with a string giving the number of quanta in each labelled normal mode.
Unspecified vibrational excitation is denoted ``v=*``. For example:

.. code-block:: pycon

    >>> from pyvalem.states import VibrationalState
    >>> v0 = VibrationalState('v=0')
    >>> v1 = VibrationalState('v=*')
    >>> v2 = VibrationalState('3v2+v3')
    >>> v3 = VibrationalState('ν1+ν2')
    >>> v4 = VibrationalState('2v1+3v4')
    >>> v5 = VibrationalState('2ν1+1ν2+ν3')

The attribute ``html`` holds an HTML representation of the vibrational state:

.. code-block:: pycon

    >>> print(v5.html)
    2ν<sub>1</sub> + ν<sub>2</sub> + ν<sub>3</sub>

This renders as:

.. raw:: html

    2ν<sub>1</sub> + ν<sub>2</sub> + ν<sub>3</sub>


``RotationalState``
===================

A single class, ``RotationalState``, represents the total rotational angular momentum
(excluding nuclear spin) quantum number, J, for both atoms and molecules.
It is instantiated with a string, ``J=n``, where ``n`` is an integer or half integer
(expressed as a fraction or in decimal notation).
Three different levels of unspecified rotation excitation may alternatively be
specified by providing ``n`` as one to three asterisks.
The parsed value of J is available as an attribute with that name.

Examples:

.. code-block:: pycon

    >>> from pyvalem.states import RotationalState
    >>> r0 = RotationalState('J=0')
    >>> r1 = RotationalState('J=3/2')
    >>> r2 = RotationalState('J=1.5')
    >>> r3 = RotationalState('J=*')
    >>> print(r1.J)
    1.5


``KeyValuePair``
================

The ``KeyValuePair`` class represents an arbitrary quantum number or symmetry provided
as a (key, value) pair. It is instantiated with a string of the form ``key=value``.
Whitespace within a key-value pair is illegal.
For example:

.. code-block:: pycon

    >>> from pyvalem.states import KeyValuePair
    >>> kv1 = KeyValuePair('n=1')
    >>> kv2 = KeyValuePair('|M|=2')
    >>> kv3 = KeyValuePair('sym=anti')
