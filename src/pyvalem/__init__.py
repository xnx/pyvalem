"""
PyValem: parse, validate and represent the chemical formulas, quantum states and
reactions of atoms, ions and small molecules.

>>> from pyvalem import Formula, Reaction, StatefulSpecies
>>> Formula("H2O+").charge
1
"""

from .formula import Formula, FormulaError, FormulaParseError
from .reaction import (
    Reaction,
    ReactionChargeError,
    ReactionParseError,
    ReactionStoichiometryError,
)
from .stateful_species import StatefulSpecies, StatefulSpeciesError

__version__ = "2.9.0.dev0"

__all__ = [
    "Formula",
    "FormulaError",
    "FormulaParseError",
    "Reaction",
    "ReactionChargeError",
    "ReactionParseError",
    "ReactionStoichiometryError",
    "StatefulSpecies",
    "StatefulSpeciesError",
    "__version__",
]
