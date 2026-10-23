"""
PyValem: parse, validate and represent the chemical formulas, quantum states and
reactions of atoms, ions and small molecules.

>>> from pyvalem import Formula, Reaction, StatefulSpecies
>>> Formula("H2O+").charge
1
"""

from .exceptions import PyValemError
from .formula import Formula, FormulaError, FormulaParseError
from .reaction import (
    Reaction,
    ReactionChargeError,
    ReactionParseError,
    ReactionStoichiometryError,
)
from .stateful_species import StatefulSpecies, StatefulSpeciesError

__version__ = "2.9.0"

__all__ = [
    "Formula",
    "FormulaError",
    "FormulaParseError",
    "PyValemError",
    "Reaction",
    "ReactionChargeError",
    "ReactionParseError",
    "ReactionStoichiometryError",
    "StatefulSpecies",
    "StatefulSpeciesError",
    "__version__",
]
