"""
PyValem: parse, validate and represent the chemical formulas, quantum states and
reactions of atoms, ions and small molecules.

>>> from pyvalem import Formula, Reaction, StatefulSpecies
>>> Formula("H2O+").charge
1
"""

from .exceptions import PyValemDeprecationWarning, PyValemError
from .formula import Formula, FormulaError, FormulaParseError, FormulaValidationError
from .reaction import (
    Reaction,
    ReactionChargeError,
    ReactionParseError,
    ReactionStoichiometryError,
)
from .stateful_species import StatefulSpecies, StatefulSpeciesError

__version__ = "3.0.2"

__all__ = [
    "Formula",
    "FormulaError",
    "FormulaParseError",
    "FormulaValidationError",
    "PyValemDeprecationWarning",
    "PyValemError",
    "Reaction",
    "ReactionChargeError",
    "ReactionParseError",
    "ReactionStoichiometryError",
    "StatefulSpecies",
    "StatefulSpeciesError",
    "__version__",
]
