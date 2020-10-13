"""
Defines dictionaries of meta data relating to the elements and their isotopes.
"""

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

# A list of all element symbols recognised by PyValem
element_symbols = [
 'H', 'He', 'Li', 'Be',  'B',  'C',  'N',  'O',  'F', 'Ne', 'Na', 'Mg', 'Al',
'Si',  'P',  'S', 'Cl', 'Ar',  'K', 'Ca', 'Sc', 'Ti',  'V', 'Cr', 'Mn', 'Fe',
'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr',  'Y',
'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',  'W', 'Re', 'Os', 'Ir', 'Pt',
'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf',
'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts',
'Og'
]

class Atom:
    is_isotope = False

    def __init__(self, symbol, name, Z, weight=None, weight_unc=None):
        self.symbol = symbol
        self.name = name
        self.Z = Z
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

    def __init__(self, Z, A, symbol, name, mass, mass_unc, estimated_flag=''):
        super().__init__(symbol, name, Z)
        self.A = A
        self.mass = mass
        self.mass_unc = mass_unc
        self.estimated_flag = estimated_flag

        self.N = A + Z

def float_or_None(f):
    """Cast string f into a float, or None if it doesn't represent a number."""

    try:
        return float(f)
    except ValueError:
        return None

def parse_aw_line(line):
    """Parse comma-separated values for atomic weight data from line."""
    fields = line.split(',')
    symbol = fields[0].strip()
    name = fields[1].strip()
    Z = int(fields[2])
    weight = float_or_None(fields[3])
    weight_unc = float_or_None(fields[4])
    return symbol, name, Z, weight, weight_unc

def parse_im_line(line):
    """Parse comma-separated values for isotope masses from line."""
    fields = line.split(',')
    Z = int(fields[0])
    A = int(fields[1])
    symbol = fields[2].strip()
    mass = float(fields[3])
    mass_unc = float(fields[4])
    estimated_flag = fields[5].strip()
    return Z, A, symbol, mass, mass_unc, estimated_flag

# Atom data is from Meija et al., "Atomic weights of the elements 2013
# (IUPAC Technical Report)", Pure Appl. Chem. 88(3), 265-291, 2016.
# See https://ciaaw.org/atomic-weights.htm
atoms = {}
with pkg_resources.open_text('pyvalem', 'atomic_weights.txt') as fi:
    # Skip the header line
    fi.readline()
    for line in fi.readlines():
        symbol, name, Z, weight, weight_unc = parse_aw_line(line)
        atoms[symbol] = Atom(symbol, name, Z, weight, weight_unc)

# Isotope data is from the AME2016 Atomic Mass Evaluation reports,
# Huang et al., "The Ame2016 atomic mass evaluation (I)", Chinese Physics C41,
# 030002 (2017); Wang et al., "The Ame2016 atomic mass evaluation (II)",
# Chinese Physics C41, 030003 (2017).
# See http://amdc.impcas.ac.cn/masstables/Ame2016/mass16.txt
isotopes = {}
with pkg_resources.open_text('pyvalem', 'isotope_masses.txt') as fi:
    # Skip the header line
    fi.readline()
    for line in fi.readlines():
        Z, A, symbol, mass, mass_unc, estimated_flag = parse_im_line(line)
        name = atoms[symbol].name + '-{}'.format(A)
        symbol = '{:d}{:s}'.format(A, symbol)
        isotopes[symbol] = Isotope(
                            Z, A, symbol, name, mass, mass_unc, estimated_flag)
