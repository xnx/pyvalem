# Examples

Short scripts that use PyValem, described in the documentation
([`docs/source/examples.rst`](../docs/source/examples.rst)). The tests run each
one and check that it prints what its file in [`output/`](output/) has.

- [`check_reactions.py`](check_reactions.py) checks a list of reactions before
  it goes into a database: their syntax and states, that they conserve atoms
  and charge, the number of electrons in atomic configurations, the g and u
  labels of diatomic ones, and duplicates.
- [`selection_rules.py`](selection_rules.py) finds the electric dipole selection
  rules that a transition between two atomic levels breaks, from the quantum
  numbers that PyValem parses from them.

With PyValem installed, run them as `python check_reactions.py`, and so on.
