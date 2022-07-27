"""
Unit tests for the formula module of PyValem
"""

import unittest

from pyvalem.formula import Formula, FormulaParseError
from .good_formulas import good_formulas


class FormulaTest(unittest.TestCase):
    def test_stoichiometric_formula_test(self):
        cf = Formula("C2F4H2")
        self.assertEqual(cf.stoichiometric_formula(), "H2C2F4")
        self.assertEqual(cf.stoichiometric_formula("alphabetical"), "C2F4H2")
        self.assertEqual(cf.stoichiometric_formula("hill"), "C2H2F4")

        cf = Formula("CFx")
        self.assertEqual(cf.stoichiometric_formula(), "CFx")
        self.assertEqual(cf.stoichiometric_formula("hill"), "CFx")

        cf = Formula("CuBr4")
        self.assertEqual(cf.stoichiometric_formula(), "CuBr4")
        self.assertEqual(cf.stoichiometric_formula("alphabetical"), "Br4Cu")
        self.assertEqual(cf.stoichiometric_formula("hill"), "Br4Cu")

        cf = Formula("HBr")
        self.assertEqual(cf.stoichiometric_formula(), "HBr")
        self.assertEqual(cf.stoichiometric_formula("alphabetical"), "BrH")
        self.assertEqual(cf.stoichiometric_formula("hill"), "BrH")

    def test_html_latex_and_slug(self):
        f = (
            ("NO+", "NO+", "NO<sup>+</sup>", r"\mathrm{N}\mathrm{O}^{+}", "NO_p"),
            ("OH-", "HO-", "OH<sup>-</sup>", r"\mathrm{O}\mathrm{H}^{-}", "OH_m"),
            (
                "CoN6H18-2",
                "H18N6Co-2",
                "CoN<sub>6</sub>H<sub>18</sub><sup>2-</sup>",
                r"\mathrm{Co}\mathrm{N}_{6}\mathrm{H}_{18}^{2-}",
                "CoN6H18_m2",
            ),
            (
                "(14N)(1H)(16O)2(18O)(16O)",
                "(1H)(14N)(16O)3(18O)",
                "<sup>14</sup>N<sup>1</sup>H<sup>16</sup>O<sub>2</sub>"
                "<sup>18</sup>O<sup>16</sup>O",
                r"{}^{14}\mathrm{N}{}^{1}\mathrm{H}{}^{16}\mathrm{O}_{2}{}^{18}\mathrm{O}{}^{16}"
                r"\mathrm{O}",
                "14N-1H-16O2-18O-16O",
            ),
            ("CFx", "CFx", "CF<sub>x</sub>", r"\mathrm{C}\mathrm{F}_{x}", "CFx"),
            ("NO+", "NO+", "NO<sup>+</sup>", r"\mathrm{N}\mathrm{O}^{+}", "NO_p"),
            ("NO+", "NO+", "NO<sup>+</sup>", r"\mathrm{N}\mathrm{O}^{+}", "NO_p"),
        )

        for formula, stoich_formula, html, latex, slug in f:
            cf = Formula(formula)
            self.assertEqual(cf.stoichiometric_formula(), stoich_formula)
            self.assertEqual(cf.html, html)
            self.assertEqual(cf.latex, latex)
            self.assertEqual(cf.slug, slug)

    def test_moieties(self):
        cf = Formula("H2NC(CH3)2CO2H")
        self.assertEqual(
            cf.html, "H<sub>2</sub>NC(CH<sub>3</sub>)" "<sub>2</sub>CO<sub>2</sub>H"
        )
        self.assertEqual(cf.slug, "H2NC-_l_CH3_r_2-CO2H")
        atom_symbols = {atom.symbol for atom in cf.atoms}
        self.assertEqual(atom_symbols, {"H", "C", "N", "O"})

        cf = Formula("Co(H2O)6+2")
        self.assertEqual(cf.html, "Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>")
        self.assertEqual(cf.latex, r"\mathrm{Co}(\mathrm{H}_{2}\mathrm{O})_{6}^{2+}")
        self.assertEqual(cf.slug, "Co-_l_H2O_r_6_p2")

    def test_good_formulas(self):
        for formula in good_formulas:
            cf = Formula(formula)
            # print(formula)
            self.assertEqual(
                cf.stoichiometric_formula(),
                good_formulas[formula]["stoichiometric_formula"],
            )
            self.assertEqual(cf.html, good_formulas[formula]["html"])
            self.assertEqual(cf.slug, good_formulas[formula]["slug"])
            self.assertAlmostEqual(cf.rmm, good_formulas[formula]["rmm"])
            if "natoms" in good_formulas[formula].keys():
                self.assertEqual(cf.natoms, good_formulas[formula]["natoms"])
            if "latex" in good_formulas[formula].keys():
                self.assertEqual(cf.latex, good_formulas[formula]["latex"])

    def test_Tc_Pm(self):
        for f in ("Tc", "Pm", "TcH", "Cl2Pm"):
            cf = Formula(f)
            self.assertIsNone(cf.rmm)

    def test_charged_species(self):
        cf1 = Formula("H+")
        self.assertEqual(cf1.html, "H<sup>+</sup>")
        self.assertEqual(cf1.charge, 1)

        self.assertRaises(FormulaParseError, Formula, "H+-")
        self.assertRaises(FormulaParseError, Formula, "H++")
        self.assertRaises(FormulaParseError, Formula, "H++2")
        self.assertRaises(FormulaParseError, Formula, "H--")
        self.assertRaises(FormulaParseError, Formula, "H+-")
        self.assertRaises(FormulaParseError, Formula, "H-+")
        self.assertRaises(FormulaParseError, Formula, "Li-2+")

        cf2 = Formula("NH2+CH3CHO2-")
        self.assertEqual(
            cf2.html,
            "NH<sub>2</sub><sup>+</sup>CH<sub>3</sub>CHO<sub>2</sub><sup>-</sup>",
        )
        self.assertEqual(cf2.charge, 0)

    def test_special_formulas(self):
        # stoichiometric_formula, html, latex, slug, rmm, natoms, charge, atoms
        f = {
            "M": ("M", "M", r"\mathrm{M}", "M", None, None, None, {"M"}),
            "e-": (
                "e-",
                "e<sup>-</sup>",
                r"\mathrm{e}^-",
                "e_m",
                5.48579909e-04,
                None,
                -1,
                {},
            ),
            "e+": (
                "e+",
                "e<sup>+</sup>",
                r"\mathrm{e}^+",
                "e_p",
                5.48579909e-04,
                None,
                1,
                {},
            ),
            "hv": ("hν", "hν", r"h\nu", "hv", 0, None, 0, {}),
        }
        f["e"] = f["e-"]
        f["hν"] = f["hv"]

        for f_str in f:
            formula = Formula(f_str)
            sf, html, latex, slug, rmm, natoms, charge, atoms = f[f_str]
            self.assertEqual(formula.stoichiometric_formula(), sf)
            self.assertEqual(formula.html, html)
            self.assertEqual(formula.latex, latex)
            self.assertEqual(formula.slug, slug)
            self.assertEqual(formula.rmm, rmm)
            self.assertEqual(formula.natoms, natoms)
            self.assertEqual(formula.charge, charge)
            self.assertEqual(formula.atoms, atoms)

    def test_parse_fail(self):
        self.assertRaises(FormulaParseError, Formula, "Mq")
        self.assertRaises(FormulaParseError, Formula, "(27N)")
        self.assertRaises(FormulaParseError, Formula, "H3O^+")
        self.assertRaises(FormulaParseError, Formula, "H_2S")

    def test_formula_hash(self):
        f1 = Formula("hv")
        f2 = Formula("Ar")
        test_dict = {f1: 0, f2: "a"}
        test_set = set((f1, f1, f2))

        f3 = Formula("hν")
        self.assertEqual(hash(f1), hash(f3))
        self.assertEqual(repr(f1), repr(f3))


if __name__ == "__main__":
    unittest.main()
