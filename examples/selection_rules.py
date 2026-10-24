"""Is an electric dipole transition between two atomic levels allowed?

PyValem parses an atomic configuration and a term symbol into the quantum numbers
that the selection rules are about: the l of each orbital, and the S, L, J and
parity of the term. A transition must change the parity, and have ΔJ = 0 or ±1 but
not J = 0 to J = 0. In LS coupling it must also have ΔS = 0, and ΔL = 0 or ±1 but
not L = 0 to L = 0.
"""

from pyvalem import StatefulSpecies
from pyvalem.states import AtomicConfiguration, AtomicTermSymbol


def parse_level(s):
    """Return the parity (0 for even, 1 for odd) and term of the atomic level s."""
    species = StatefulSpecies(s)
    # A level has one configuration and one term symbol.
    (config,) = species.get_states_of_type(AtomicConfiguration)
    (term,) = species.get_states_of_type(AtomicTermSymbol)
    parity = sum(orbital.l * orbital.nocc for orbital in config.orbitals) % 2
    if parity != (term.parity == "o"):
        raise ValueError(f"{s}: the parity of the term isn't that of the configuration")
    return parity, term


def broken_rules(level1, level2):
    """Return the selection rules broken by a transition between two levels."""
    (parity1, term1), (parity2, term2) = parse_level(level1), parse_level(level2)
    broken = []
    if parity1 == parity2:
        broken.append("no change of parity")
    if abs(term1.J - term2.J) > 1:
        broken.append(f"ΔJ = {abs(term1.J - term2.J):g}")
    elif term1.J == term2.J == 0:
        broken.append("J = 0 to J = 0")
    if term1.S != term2.S:
        broken.append(f"ΔS = {abs(term1.S - term2.S):g}")
    if abs(term1.L - term2.L) > 1:
        broken.append(f"ΔL = {abs(term1.L - term2.L)}")
    elif term1.L == term2.L == 0:
        broken.append("L = 0 to L = 0")
    return broken


TRANSITIONS = [
    ("Na 3s 2S_1/2", "Na 3p 2Po_3/2", "the sodium D2 line, 589.0 nm"),
    ("Hg 6s2 1S_0", "Hg 6s.6p 3Po_1", "the main line of a mercury lamp, 253.7 nm"),
    ("O 2p4 1D_2", "O 2p4 1S_0", "the green line of the aurora, 557.7 nm"),
    ("O 2p4 3P_2", "O 2p4 1D_2", "the red line of the aurora, 630.0 nm"),
    ("He 1s2 1S_0", "He 1s.2s 1S_0", "helium, 60.1 nm"),
]

if __name__ == "__main__":
    for level1, level2, name in TRANSITIONS:
        print(f"{level1} – {level2} ({name})")
        print("   ", "; ".join(broken_rules(level1, level2)) or "allowed")

    # The parity of a term must be that of its configuration.
    try:
        parse_level("O 2p4 3Po_2")
    except ValueError as err:
        print(err)
