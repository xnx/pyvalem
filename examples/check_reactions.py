"""Check a list of reactions before it goes into a database.

Each reaction is parsed, which checks the syntax of its formulas and states and
that it conserves atoms and charge. Its species are then checked for the number
of electrons in an atomic configuration, and for the g and u labels of a diatomic
configuration. A reaction whose canonical form is that of an earlier one is
reported as a duplicate.

Run it on a file of reactions, one to a line, or with no file on the sample below:

    python check_reactions.py [reactions.txt]

Blank lines, and lines starting with #, are ignored.
"""

import sys

from pyvalem import PyValemError, Reaction

SAMPLE = """\
e- + Ar -> Ar+ + 2e-
e- + Ar -> e- + Ar*
e- + N2 X(1Σ+g) v=0 -> e- + N2 X(1Σ+g) v=1
e- + CO2 -> CO + O
e- + H2O -> H- + O
e- + He+ 1s2 -> He + hν
Ar+ 2P_5/2 + e- -> Ar + hν
e- + CO 1σg2 -> e- + CO
e- + N2 X(1SIGMA+g) v=0 -> N2 v=1;X(1Σ+g) + e-
"""


def check(lines):
    """Print the problems with the reactions in lines."""
    first_seen = {}
    for lineno, line in enumerate(lines, start=1):
        if not line.strip() or line.startswith("#"):
            continue
        try:
            reaction = Reaction(line)
            # StatefulSpecies doesn't make these checks itself.
            for _, species in reaction.reactants + reaction.products:
                species.verify_atomic_configuration()
                species.verify_diatomic_inversion_parity()
        except PyValemError as err:
            print(f"line {lineno}: {err}")
            continue
        # The line on which a reaction with this canonical form first appeared.
        first = first_seen.setdefault(repr(reaction), lineno)
        if first != lineno:
            print(f"line {lineno}: the same as line {first}: {reaction!r}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf8") as f:
            check(f.read().splitlines())
    else:
        check(SAMPLE.splitlines())
