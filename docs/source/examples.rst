Examples
********

These scripts are in the ``examples`` directory of the PyValem repository. The
tests run them and check that they still print what is shown here.


Checking a list of reactions
============================

A list of reactions put together by hand, or converted from another format, is
likely to have mistakes in it. This script reports the reactions in a list that:

* can't be parsed, such as ``e- + Ar -> e- + Ar*``: in PyValem's notation, a
  state is separated from its formula by a space, as in ``Ar *``;
* don't conserve atoms or charge;
* have an invalid state, such as a term symbol with an impossible J;
* have an atomic configuration with the wrong number of electrons for its atom
  or ion, or a diatomic configuration whose g and u labels don't fit its
  molecule. ``StatefulSpecies`` doesn't check these itself, so the script calls
  ``verify_atomic_configuration()`` and ``verify_diatomic_inversion_parity()``;
* are the same as an earlier reaction, however differently they are written.

.. literalinclude:: ../../examples/check_reactions.py
   :language: python

Run on its sample, it prints:

.. literalinclude:: ../../examples/output/check_reactions.txt
   :language: text

Line 9 is written ``e- + N2 X(1SIGMA+g) v=0 -> N2 v=1;X(1Σ+g) + e-``, but its
canonical form (its ``repr()``) is that of line 3. The canonical form of a
reaction keeps its species in the order they are written, apart from electrons,
positrons and photons, so ``H2 + O2 -> H2O2`` and ``O2 + H2 -> H2O2`` are not
counted as the same.


Selection rules for atomic transitions
======================================

PyValem parses states into their quantum numbers, so it can do more than check
the notation. This script finds the electric dipole selection rules that a
transition between two atomic levels breaks, from the parity of each level's
configuration and the S, L and J of its term.

.. literalinclude:: ../../examples/selection_rules.py
   :language: python

It prints:

.. literalinclude:: ../../examples/output/selection_rules.txt
   :language: text

The sodium D2 line is allowed. The mercury line at 253.7 nm breaks the rule
that ΔS = 0, but that rule holds only in LS coupling, which breaks down in heavy
atoms: this is the main line of a low-pressure mercury lamp. The green and red
lines of the aurora are forbidden. Their upper levels live for about a second
and about two minutes, so these lines are seen only high in the atmosphere,
where collisions are too rare to de-excite the atoms first. The 1s.2s 1S_0
level of helium can't decay to the ground state by emitting one photon, so it
emits two.

The last line shows the same parser checking data: ``2p4`` is an even
configuration, so its terms can't have odd parity.


Labels for plots
================

PyValem's LaTeX is for math mode, which Matplotlib's mathtext renders without a
TeX installation, so a plot can be labelled from the reactions or species it
shows:

.. code-block:: python

    import matplotlib.pyplot as plt

    from pyvalem import Reaction


    def plot_cross_sections(data):
        """Plot cross sections, given as {reaction: (energies, cross sections)}."""
        fig, ax = plt.subplots()
        for reaction, (energy, sigma) in data.items():
            ax.plot(energy, sigma, label=f"${Reaction(reaction).latex}$")
        ax.set_xlabel("Energy (eV)")
        ax.set_ylabel(r"Cross section (cm$^2$)")
        ax.legend()
        return fig

The legend then shows ``e- + N2 X(1Σ+g) v=0 -> e- + N2 X(1Σ+g) v=1`` typeset,
with its subscripts, superscripts and arrow.
