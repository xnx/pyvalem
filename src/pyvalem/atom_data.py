"""
Defines dictionaries of meta data relating to the elements and their isotopes.
"""

import csv

try:
    import importlib.resources as pkg_resources
except ImportError:
    # for python < 3.7, use the importlib-resources backport
    # noinspection PyUnresolvedReferences
    import importlib_resources as pkg_resources


class Atom:
    is_isotope = False

    def __init__(self, symbol, name, atomic_number, weight=None, weight_unc=None):
        self.symbol = symbol
        self.name = name
        self.Z = atomic_number
        self.weight = self.mass = weight
        self.weight_unc = weight_unc

    def __repr__(self):
        return self.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.symbol == other.symbol
        return self.symbol == other


class Isotope(Atom):
    is_isotope = True

    def __init__(
        self,
        atomic_number,
        mass_number,
        symbol,
        name,
        mass,
        mass_unc,
        estimated_flag="",
    ):
        super().__init__(symbol, name, atomic_number)
        self.A = mass_number
        self.mass = mass
        self.mass_unc = mass_unc
        self.estimated_flag = estimated_flag
        self.N = mass_number + atomic_number


def float_or_none(f):
    """
    Cast string f into a float, or None if it doesn't represent a number.
    """
    try:
        return float(f)
    except ValueError:
        return None


# list of all the element symbols recognised by pyvalem:
element_symbols = []
# pre-built mapping between element symbols and Atom instances:
atoms = {}
# Atom data is from Meija et al., "Atomic weights of the elements 2013
# (IUPAC Technical Report)", Pure Appl. Chem. 88(3), 265-291, 2016.
# See https://ciaaw.org/atomic-weights.htm
with pkg_resources.open_text("pyvalem", "atomic_weights.txt") as fi:
    reader = csv.reader(fi, delimiter=",")
    header = ["Symbol", "Name", "Z", "atomic_weight", "atomic_weight_unc"]
    for row in reader:
        row = [val.strip() for val in row]
        if row == header:
            continue  # skip the header
        atom_dtypes = [str, str, int, float_or_none, float_or_none]
        atom_args = [dtype(val) for dtype, val in zip(atom_dtypes, row)]
        element_symbol = atom_args[0]
        element_symbols.append(element_symbol)
        atoms[element_symbol] = Atom(*atom_args)

# pre-built mapping between element isotopic symbols and Isotope instances:
isotopes = {}
# Isotope data is from the AME2016 Atomic Mass Evaluation reports,
# Huang et al., "The Ame2016 atomic mass evaluation (I)", Chinese Physics C41,
# 030002 (2017); Wang et al., "The Ame2016 atomic mass evaluation (II)",
# Chinese Physics C41, 030003 (2017).
# See http://amdc.impcas.ac.cn/masstables/Ame2016/mass16.txt
with pkg_resources.open_text("pyvalem", "isotope_masses.txt") as fi:
    reader = csv.reader(fi, delimiter=",")
    header = ["Z", "A", "Symbol", "mass", "mass_unc", "estimated_flag"]
    iso_attribs = [
        "atomic_number",
        "mass_number",
        "symbol",
        "mass",
        "mass_unc",
        "estimated_flag",
    ]
    for row in reader:
        row = [val.strip() for val in row]
        if row == header:
            continue
        iso_dtypes = [int, int, str, float, float, str]
        iso_kwargs = {
            attr: dtype(val) for attr, dtype, val in zip(iso_attribs, iso_dtypes, row)
        }
        iso_name = "{}-{}".format(
            atoms[iso_kwargs["symbol"]].name, iso_kwargs["mass_number"]
        )
        iso_kwargs["name"] = iso_name
        iso_symbol = "{:d}{:s}".format(iso_kwargs["mass_number"], iso_kwargs["symbol"])
        iso_kwargs["symbol"] = iso_symbol
        isotopes[iso_symbol] = Isotope(**iso_kwargs)
