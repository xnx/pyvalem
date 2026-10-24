"""
Unit tests for the formula module of PyValem
"""

import unittest

from pyvalem.formula import Formula, FormulaParseError, FormulaValidationError

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

    def test_stoichiometric_formula_with_isotopes(self):
        # Isotopes are listed with their element, after the element itself.
        cases = {
            "(13C)H3Cl": ("H3(13C)Cl", "(13C)ClH3", "(13C)H3Cl"),
            "HDO": ("H(2H)O", "H(2H)O", "H(2H)O"),
            "DCl": ("(2H)Cl", "Cl(2H)", "Cl(2H)"),
            "CH3D": ("H3(2H)C", "CH3(2H)", "CH3(2H)"),
            "H(1H)": ("H(1H)", "H(1H)", "H(1H)"),
        }
        for s, (atomic_number, alphabetical, hill) in cases.items():
            with self.subTest(s):
                f = Formula(s)
                self.assertEqual(f.stoichiometric_formula(), atomic_number)
                self.assertEqual(f.stoichiometric_formula("alphabetical"), alphabetical)
                self.assertEqual(f.stoichiometric_formula("hill"), hill)

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

    def test_prefixes_and_deuterium(self):
        # D is both a prefix and deuterium: a prefix must be followed by a moiety.
        self.assertEqual(Formula("D-").charge, -1)
        self.assertEqual(Formula("D-2").charge, -2)
        self.assertEqual(Formula("D-H").atom_stoich, {"H": 1})
        self.assertEqual(Formula("trans-D").atom_stoich, {"2H": 1})
        self.assertEqual(Formula("trans-D1"), Formula("trans-D"))
        self.assertEqual(Formula("D-D").atom_stoich, {"2H": 1})

    def test_prefix_latex(self):
        self.assertEqual(
            Formula("(±)-CHClBrF").latex,
            r"(\pm)-\mathrm{C}\mathrm{H}\mathrm{Cl}\mathrm{Br}\mathrm{F}",
        )

    def test_moieties(self):
        cf = Formula("H2NC(CH3)2CO2H")
        self.assertEqual(
            cf.html, "H<sub>2</sub>NC(CH<sub>3</sub>)<sub>2</sub>CO<sub>2</sub>H"
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
            if "natoms" in good_formulas[formula]:
                self.assertEqual(cf.natoms, good_formulas[formula]["natoms"])
            if "latex" in good_formulas[formula]:
                self.assertEqual(cf.latex, good_formulas[formula]["latex"])

    def test_elements_without_atomic_weight_and_their_isotopes(self):
        f = Formula("Tc(98Tc)")
        self.assertEqual(f.stoichiometric_formula(), "Tc(98Tc)")
        self.assertIsNone(f.rmm)

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

        cf2 = Formula("(NH2+)CH3CHO2-")
        self.assertEqual(
            cf2.html,
            "(NH<sub>2</sub><sup>+</sup>)CH<sub>3</sub>CHO<sub>2</sub><sup>-</sup>",
        )
        self.assertEqual(cf2.charge, 0)

    def test_numeric_locant_prefixes(self):
        for s in ("trans-2-C4H8", "cis-2-C4H8", "(+)-2-C4H9Cl", "(R)-2-C4H9Cl"):
            with self.subTest(s):
                self.assertEqual(Formula(s).charge, 0)
        self.assertEqual(Formula("trans-2-C4H8").slug, "trans_2__C4H8")
        # Consecutive numeric prefixes are invalid: locants are comma-separated.
        for s in ("1-1-C2H4Cl2", "1,1-2-C2H3Cl3", "cis-1-2-CHFCHF"):
            with self.subTest(s):
                self.assertRaises(FormulaParseError, Formula, s)

    def test_second_charge(self):
        for s in ("Li+2-", "Li-2+", "Li+2+3", "Li+2+0", "H2O+2-", "(H2O+)2+-"):
            with self.subTest(s):
                self.assertRaises(FormulaParseError, Formula, s)
        self.assertEqual(Formula("(H2O)2+").charge, 1)

    def test_invalid_syntax(self):
        invalid = {
            "whitespace": ("H2 O", " H2O", "H2O ", "Ca (OH)2", "H2O +"),
            "leading zeros and zero counts": (
                "H02",
                "H0",
                "0H2O",
                "(H2O)0",
                "Ar+02",
                "H2O+0",
                "(013C)",
                "01,1-C2H4Cl2",
            ),
            "unbracketed charge before the end": (
                "NH2+CH3CHO2-",
                "NH2-CH3",
                "H+CH3",
                "Na+.Cl-",
            ),
            "conflicting charges": ("(H2O+)2+", "(NH4+)2(SO4)-2"),
            "separators": (".H2O", "H2O.", "H2O..H2O"),
        }
        for reason, formulas in invalid.items():
            for s in formulas:
                with self.subTest(reason=reason, formula=s):
                    with self.assertRaises(FormulaParseError) as cm:
                        Formula(s)
                    self.assertNotIsInstance(cm.exception, FormulaValidationError)

    def test_invalid_species(self):
        for s in ("(99H)", "(27N)", "(NH4+)x"):
            with self.subTest(s):
                self.assertRaises(FormulaValidationError, Formula, s)

    def test_canonical_form(self):
        canonical = {
            "H+1": "H+",
            "OH-1": "OH-",
            "H1": "H",
            "1H2O": "H2O",
            "(H2O)1": "(H2O)",
            "1(H2O)": "(H2O)",
            "Co(H2O)6+2": "Co(H2O)6+2",
            "SiO2.1H2O": "SiO2.H2O",
            "D-": "D-",
            "D2O": "D2O",
            "(2H)2O": "(2H)2O",
            "cis-1,2-CHFCHF": "cis-1,2-CHFCHF",
            "e": "e-",
            "hv": "hν",
        }
        for s, expected in canonical.items():
            with self.subTest(s):
                f = Formula(s)
                self.assertEqual(repr(f), expected)
                self.assertEqual(Formula(expected), f)
        self.assertEqual(Formula("H+1"), Formula("H+"))
        self.assertNotEqual(Formula("D"), Formula("(2H)"))

    def test_radical_dot_rendering(self):
        # The dot goes where it is written: after the atoms, before any charge.
        f = Formula("OH·-")
        self.assertEqual(f.html, "OH&#183;<sup>-</sup>")
        self.assertEqual(f.latex, r"\mathrm{O}\mathrm{H}\cdot^{-}")
        f = Formula("(OH·)2")
        self.assertEqual(f.html, "(OH&#183;)<sub>2</sub>")
        self.assertEqual(f.slug, "_l_OH_r_2_dot")

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
                set(),
            ),
            "e+": (
                "e+",
                "e<sup>+</sup>",
                r"\mathrm{e}^+",
                "e_p",
                5.48579909e-04,
                None,
                1,
                set(),
            ),
            "hv": ("hν", "hν", r"h\nu", "hv", 0, None, 0, set()),
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

    def test_special_formulas_are_independent(self):
        f1 = Formula("e-")
        f1.atom_stoich["X"] = 1
        f1.atoms.add("X")
        f2 = Formula("e-")
        self.assertEqual(f2.atom_stoich, {})
        self.assertEqual(f2.atoms, set())

    def test_parse_fail(self):
        self.assertRaises(FormulaParseError, Formula, "Mq")
        self.assertRaises(FormulaParseError, Formula, "(27N)")
        self.assertRaises(FormulaParseError, Formula, "H3O^+")
        self.assertRaises(FormulaParseError, Formula, "H_2S")

    def test_unspecified_stoichiometry(self):
        f = Formula("CxH4")
        self.assertIsNone(f.natoms)
        self.assertIsNone(f.rmm)
        self.assertEqual(dict(f.atom_stoich), {"C": None, "H": 4})
        self.assertEqual(f.html, "C<sub>x</sub>H<sub>4</sub>")
        self.assertEqual(f.stoichiometric_formula("hill"), "CxH4")

        f = Formula("FxC")
        self.assertEqual(dict(f.atom_stoich), {"F": None, "C": 1})

        f = Formula("(CH2)x")
        self.assertIsNone(f.natoms)
        self.assertEqual(dict(f.atom_stoich), {"C": None, "H": None})
        self.assertEqual(f.html, "(CH<sub>2</sub>)<sub>x</sub>")
        self.assertEqual(f.latex, r"(\mathrm{C}\mathrm{H}_{2})_{x}")
        self.assertEqual(f.slug, "_l_CH2_r_x")

        f = Formula("CuSO4.xH2O")
        self.assertIsNone(f.rmm)
        self.assertEqual(dict(f.atom_stoich), {"Cu": 1, "S": 1, "O": None, "H": None})
        self.assertEqual(f.html, "CuSO<sub>4</sub>&#183;xH<sub>2</sub>O")
        self.assertEqual(
            f.latex,
            r"\mathrm{Cu}\mathrm{S}\mathrm{O}_{4}\cdot x\mathrm{H}_{2}\mathrm{O}",
        )

        # The charge of a charged moiety with an unspecified count is undefined.
        self.assertRaises(FormulaParseError, Formula, "(NH4+)x")
        self.assertRaises(FormulaParseError, Formula, "xNH4+")

    def test_comparison_with_other_types(self):
        self.assertNotEqual(Formula("H2"), "H2")
        self.assertNotEqual(Formula("H2"), None)

    def test_formula_hash(self):
        f1 = Formula("hv")
        f2 = Formula("Ar")
        test_dict = {f1: 0, f2: "a"}
        test_set = {f1, f1, f2}

        f3 = Formula("hν")
        self.assertEqual(hash(f1), hash(f3))
        self.assertEqual(repr(f1), repr(f3))


if __name__ == "__main__":
    unittest.main()
