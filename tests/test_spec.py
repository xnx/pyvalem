"""
Run the test vectors of the specification of the PyValem notation, in spec/tests/.
"""

import json
import math
import unittest
from pathlib import Path

from pyvalem import (
    Formula,
    FormulaValidationError,
    PyValemError,
    Reaction,
    ReactionChargeError,
    ReactionStoichiometryError,
    StatefulSpecies,
    StatefulSpeciesError,
)
from pyvalem.states import StateValidationError
from pyvalem.states._state_parser import state_parser

SPEC_TESTS = Path(__file__).parents[1] / "spec" / "tests"


def load(name):
    """Return the cases in the test vector file name."""
    if not SPEC_TESTS.exists():
        raise unittest.SkipTest("the specification's test vectors are not available")
    with open(SPEC_TESTS / name, encoding="utf8") as f:
        return json.load(f)["tests"]


def error_kind(err):
    """Return the kind of an error, from the exception or those that caused it."""
    while err is not None:
        if isinstance(err, ReactionStoichiometryError):
            return "stoichiometry"
        if isinstance(err, ReactionChargeError):
            return "charge"
        if isinstance(
            err, (StateValidationError, FormulaValidationError, StatefulSpeciesError)
        ):
            return "validation"
        err = err.__cause__
    return "syntax"


class SpecTest(unittest.TestCase):
    def check(self, case, parse, properties):
        """Check that parse(case) has the error or properties given by case."""
        if "error" in case:
            with self.assertRaises(PyValemError) as cm:
                parse(case)
            self.assertEqual(error_kind(cm.exception), case["error"])
            return
        result = parse(case)
        for name, value in properties(result).items():
            if name in case:
                self.assertEqual(value, case[name], name)

    def test_formulas(self):
        def properties(f):
            return {
                "canonical": repr(f),
                "charge": f.charge,
                "natoms": f.natoms,
                "atoms": dict(f.atom_stoich),
                "stoichiometric": {
                    fmt: f.stoichiometric_formula(fmt)
                    for fmt in ("atomic number", "alphabetical", "hill")
                },
                "html": f.html,
                "latex": f.latex,
                "slug": f.slug,
            }

        for case in load("formulas.json"):
            with self.subTest(case["input"]):
                self.check(case, lambda case: Formula(case["input"]), properties)
                if "mass" in case:
                    mass = Formula(case["input"]).mass
                    if case["mass"] is None:
                        self.assertIsNone(mass)
                    else:
                        self.assertTrue(math.isclose(mass, case["mass"], rel_tol=1e-9))

    def test_states(self):
        def properties(state):
            return {
                "type": type(state).__name__,
                "canonical": repr(state),
                "html": state.html,
                "latex": state.latex,
            }

        for case in load("states.json"):
            with self.subTest(case["input"]):
                self.check(case, lambda case: state_parser(case["input"]), properties)

    def test_species(self):
        def properties(species):
            return {
                "canonical": repr(species),
                "formula": repr(species.formula),
                "states": [
                    {"type": type(state).__name__, "canonical": repr(state)}
                    for state in species.states
                ],
                "html": species.html,
                "latex": species.latex,
            }

        for case in load("species.json"):
            with self.subTest(case["input"]):
                self.check(
                    case, lambda case: StatefulSpecies(case["input"]), properties
                )

    def test_reactions(self):
        def parse(case):
            return Reaction(case["input"], strict=case.get("strict", True))

        def properties(reaction):
            return {
                "canonical": repr(reaction),
                "reactants": [[n, repr(ss)] for n, ss in reaction.reactants],
                "products": [[n, repr(ss)] for n, ss in reaction.products],
                "html": reaction.html,
                "latex": reaction.latex,
            }

        for case in load("reactions.json"):
            with self.subTest(case["input"]):
                self.check(case, parse, properties)

    def test_canonical_forms_round_trip(self):
        # Parsing a canonical form gives the same canonical form (section 1).
        for name, parse in (
            ("formulas.json", Formula),
            ("states.json", state_parser),
            ("species.json", StatefulSpecies),
        ):
            for case in load(name):
                if "canonical" in case:
                    with self.subTest(file=name, input=case["input"]):
                        self.assertEqual(
                            repr(parse(case["canonical"])), case["canonical"]
                        )


if __name__ == "__main__":
    unittest.main()
