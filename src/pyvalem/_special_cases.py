"""
Special cases of formulas for particular species.

The keys of the inner dictionaries are attribute names of the resulting Formula
class instance, and are assigned to the corresponding values.
"""

special_cases = {
    "M": {
        "slug": "M",
        "html": "M",
        "latex": r"\mathrm{M}",
        "atom_stoich": {},
        "mass": None,
        "rmm": None,
        "charge": None,
        "natoms": None,
        "atoms": {"M"},
        "name": "generic third body",
    },
    "hν": {
        "slug": "hv",
        "html": "hν",
        "latex": r"h\nu",
        "atom_stoich": {},
        "mass": 0,
        "rmm": 0,
        "charge": 0,
        "natoms": None,
        "atoms": {},
        "name": "photon",
    },
    "e-": {
        "slug": "e_m",
        "html": "e<sup>-</sup>",
        "latex": r"\mathrm{e}^-",
        "atom_stoich": {},
        "mass": 5.48579909e-04,  # m_e / u
        "rmm": 5.48579909e-04,  # m_e / u
        "charge": -1,
        "natoms": None,
        "atoms": {},
        "name": "electron",
    },
    "e+": {
        "slug": "e_p",
        "html": "e<sup>+</sup>",
        "latex": r"\mathrm{e}^+",
        "atom_stoich": {},
        "mass": 5.48579909e-04,  # m_(e+) / u
        "rmm": 5.48579909e-04,  # m_(e+) / u
        "charge": 1,
        "natoms": None,
        "atoms": {},
        "name": "positron",
    },
}
special_cases["hv"] = special_cases["hν"]
