"""This module defines dictionaries of meta data relating to the elements and
their isotopes.

Routine Listings
----------------
atoms : dict[str, Atom]
    Dictionary of `Atom` instances keyed by the elemental symbols.
isotopes : dict[str, Isotope]:
    Dictionary of `Isotope` instances. Keys are in the form of mass number followed by
    the element symbol, such as ``"38Ar"``

Notes
-----
The atomic data are compiled from Meija et al.[1]_.
The isotope data are compiled from the AME2016 Atomic Mass Evaluation reports[2]_.

References
----------
.. [1] Meija et al., "Atomic weights of the elements 2013
   (IUPAC Technical Report)", Pure Appl. Chem. 88(3), 265-291, 2016.
   See https://ciaaw.org/atomic-weights.htm
.. [2] Huang et al., "The Ame2016 atomic mass evaluation (I)", Chinese Physics C41,
   030002 (2017); Wang et al., "The Ame2016 atomic mass evaluation (II)",
   Chinese Physics C41, 030003 (2017).
   See http://amdc.impcas.ac.cn/masstables/Ame2016/mass16.txt

Examples
--------
>>> ar_atom = atoms["Ar"]
>>> ar_atom.name
'Argon'
>>> ar_atom.Z
18

>>> ar_isotope = isotopes["38Ar"]
>>> ar_isotope.A, ar_isotope.N
(38, 20)
"""

import csv
import platform

try:
    import importlib.resources as pkg_resources
except ImportError:
    # for python < 3.7, use the importlib-resources backport
    # noinspection PyUnresolvedReferences
    import importlib_resources as pkg_resources

PYTHON3_VERSION = int(platform.python_version_tuple()[1])


class Atom:
    """Class representing an atom instance.

    All the parameters are stored as instance attributes.
    The `Atom` instances are hashable.

    Parameters
    ----------
    symbol, name : str
        Element symbol and name, such as ``"Ar"``, ``"Argon"``.
    atomic_number : int
        Z number of the atom.
    weight, weight_unc : float, optional
        Atomic weight in [amu] and the uncertainty.

    Attributes
    ----------
    symbol, name : str
    Z : int
    weight, weight_unc : float or NoneType

    Examples
    --------
    >>> atom = Atom("Ar", "Argon", 18)
    >>> atom == "Ar"
    True
    >>> atom.is_isotope
    False
    """

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
    """Class representing an isotope instance.

    The `Isotope` instances are hashable.

    Parameters
    ----------
    atomic_number : int
        Atomic number Z of the isotope.
    mass_number : int
        Mass number A of the isotope.
    symbol, name : str
        Element symbol and name, such as ``"Ar"``, ``"Argon"``.
    mass, mass_unc : float
        Atomic weight in [amu] and the uncertainty.
    estimated_flag : str
        Generic field flagging estimated values.

    Attributes
    ----------
    A : int
    mass, mass_unc : float
    estimated_flag : str
    N : int
        A + Z

    Examples
    --------
    >>> isotope = Isotope(18, 38, "Ar", "Argon", 37.9627321040, 2.09e-07)
    >>> isotope.is_isotope
    True
    >>> isotope.A
    38
    >>> isotope.N
    20
    """

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
        self.N = mass_number - atomic_number


def float_or_none(f):
    """Cast string ``f`` into a float, or None if it doesn't represent a number.

    Parameters
    ----------
    f : Any

    Returns
    -------
    float or NoneType
    """
    try:
        return float(f)
    except ValueError:
        return None


def read_atom_data(fi, atoms):
    """
    Read atom data from open file handle fi into dictionary atoms, keyed by
    element symbol.
    """

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
    return atoms


# list of all the element symbols recognised by pyvalem:
element_symbols = []
# pre-built mapping between element symbols and Atom instances:
atoms = {}
# Atom data is from Meija et al., "Atomic weights of the elements 2013
# (IUPAC Technical Report)", Pure Appl. Chem. 88(3), 265-291, 2016.
# See https://ciaaw.org/atomic-weights.htm
if PYTHON3_VERSION < 9:
    # NB Python 3.8 and below use open_text:
    with pkg_resources.open_text("pyvalem", "_data_atomic_weights.txt") as fi:
        read_atom_data(fi, atoms)
else:
    # NB Python 3.9 and above use importlib.resources.files:
    with pkg_resources.files("pyvalem").joinpath("_data_atomic_weights.txt").open(
        "r", encoding="utf8"
    ) as fi:
        read_atom_data(fi, atoms)


def read_isotope_data(fi, isotopes):
    """
    Read in isotope mass data from open file handle fi into dictionary isotopes,
    keyed by isotope symbol (e.g. "46Ti").
    """

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


# pre-built mapping between element isotopic symbols and Isotope instances:
isotopes = {}
# Isotope data is from the AME2016 Atomic Mass Evaluation reports,
# Huang et al., "The Ame2016 atomic mass evaluation (I)", Chinese Physics C41,
# 030002 (2017); Wang et al., "The Ame2016 atomic mass evaluation (II)",
# Chinese Physics C41, 030003 (2017).
# See http://amdc.impcas.ac.cn/masstables/Ame2016/mass16.txt
if PYTHON3_VERSION < 9:
    # NB Python 3.8 and below use open_text:
    with pkg_resources.open_text("pyvalem", "_data_isotope_masses.txt") as fi:
        read_isotope_data(fi, isotopes)
else:
    # NB Python 3.9 and above use importlib.resources.files:
    with pkg_resources.files("pyvalem").joinpath("_data_isotope_masses.txt").open(
        "r", encoding="utf8"
    ) as fi:
        read_isotope_data(fi, isotopes)
