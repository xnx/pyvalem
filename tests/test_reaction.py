"""
# Unit tests for the reaction module of PyValem
"""

import unittest

from pyvalem.reaction import (
    Reaction,
    ReactionParseError,
    ReactionStoichiometryError,
    ReactionChargeError,
)


class ReactionParseTest(unittest.TestCase):
    def setUp(self):
        self.r_strings = [
            "e- + 2H -> e- + H + H",
            "H + hv → hv + H+ + e-",
            "2H + He + 2H -> He + 4H",
            "e+ + H + hv → H+",
            "H + H + e- + 2H <-> e- + e- + 4H + e+ + hv",
            "W+26 + M -> e- + W+28 + M + e-",
        ]
        self.expected_repr = [
            "e- + H + H → H + H + e-",
            "hν + H → H+ + hν + e-",
            "H + H + He + H + H → He + H + H + H + H",
            "e+ + hν + H → H+",
            "e- + H + H + H + H ⇌ H + H + H + H + hν + 2e- + e+",
            "W+26 + M → W+28 + M + 2e-",
        ]
        self.expected_html = [
            "e<sup>-</sup> + 2H → e<sup>-</sup> + H + H",
            "H + hν → hν + H<sup>+</sup> + e<sup>-</sup>",
            "2H + He + 2H → He + 4H",
            "e<sup>+</sup> + H + hν → H<sup>+</sup>",
            "H + H + e<sup>-</sup> + 2H ⇌ "
            "e<sup>-</sup> + e<sup>-</sup> + 4H + e<sup>+</sup> + hν",
            "W<sup>26+</sup> + M → e<sup>-</sup> + W<sup>28+</sup> + M + e<sup>-</sup>",
        ]
        self.expected_latex = [
            r"\mathrm{e}^- + 2\mathrm{H} \rightarrow "
            r"\mathrm{e}^- + \mathrm{H} + \mathrm{H}",
            r"\mathrm{H} + h\nu \rightarrow h\nu + \mathrm{H}^{+} + \mathrm{e}^-",
            r"2\mathrm{H} + \mathrm{He} + 2\mathrm{H} \rightarrow "
            r"\mathrm{He} + 4\mathrm{H}",
            r"\mathrm{e}^+ + \mathrm{H} + h\nu \rightarrow \mathrm{H}^{+}",
            r"\mathrm{H} + \mathrm{H} + \mathrm{e}^- + 2\mathrm{H} \rightlefthooks "
            r"\mathrm{e}^- + \mathrm{e}^- + 4\mathrm{H} + \mathrm{e}^+ + h\nu",
            r"\mathrm{W}^{26+} + \mathrm{M} \rightarrow "
            r"\mathrm{e}^- + \mathrm{W}^{28+} + \mathrm{M} + \mathrm{e}^-",
        ]

    def test_reaction_parsing(self):
        s_r1 = "CO + O2 → CO2 + O"
        r1 = Reaction(s_r1)
        self.assertEqual(str(r1), s_r1)
        r2 = Reaction("CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O")
        self.assertEqual(str(r2), "CO v=1 + O2 X(3Σ-g);J=2 → CO2 + O")
        self.assertRaises(ReactionParseError, Reaction, "CO + O2 CO2 + O")
        self.assertRaises(ReactionParseError, Reaction, "CO + O2 = + CO2 + O")
        self.assertRaises(ReactionParseError, Reaction, "BeH+ + I2 =⇌ BeI")
        self.assertRaises(ReactionStoichiometryError, Reaction, "BeH + I2 ⇌ BeI")
        self.assertRaises(ReactionChargeError, Reaction, "BeH+ + I2 ⇌ BeI + HI")
        self.assertEqual(r1.reactants[0][1].__repr__(), "CO")
        self.assertEqual(r2.reactants[0][1].states[0].__repr__(), "v=1")
        self.assertEqual(r2.reactants[1][1].states[1].__repr__(), "X(3Σ-g)")
        self.assertEqual(
            r2.html,
            "CO v=1 + O<sub>2</sub> J=2 "
            "X<sup>3</sup>Σ<sup>-</sup><sub>g</sub> → "
            "CO<sub>2</sub> + O",
        )
        self.assertEqual(
            r2.latex,
            r"\mathrm{C}\mathrm{O} \; v=1 + "
            r"\mathrm{O}_{2} \; J=2 \; "
            r"X{}^{3}\Sigma^-_{g} \rightarrow "
            r"\mathrm{C}\mathrm{O}_{2} + \mathrm{O}",
        )

        s_r3 = "C6H5OH + 7O2 -> 6CO2 + 3H2O"
        r3 = Reaction(s_r3)
        self.assertEqual(str(r3), "C6H5OH + 7O2 → 6CO2 + 3H2O")
        self.assertEqual(
            r3.latex,
            r"\mathrm{C}_{6}\mathrm{H}_{5}\mathrm{O}"
            r"\mathrm{H} + 7\mathrm{O}_{2} "
            r"\rightarrow 6\mathrm{C}"
            r"\mathrm{O}_{2} + "
            r"3\mathrm{H}_{2}\mathrm{O}",
        )

        s_r4 = "7O2 + C6H5OH -> 6CO2 + 3H2O"
        r4 = Reaction(s_r4)
        self.assertNotEqual(r3, r4)

    def test_incomplete_reaction(self):
        self.assertRaises(ReactionParseError, Reaction, "Ar+ + He ->")
        self.assertRaises(ReactionParseError, Reaction, "Ar+ + He -> ")
        r1 = Reaction("Ar+ + He ->", strict=False)
        r2 = Reaction("Ar+ + He -> ", strict=False)

        self.assertEqual(str(r1), "Ar+ + He →")
        self.assertEqual(r1.html, "Ar<sup>+</sup> + He →")
        self.assertEqual(r1.latex, r"\mathrm{Ar}^{+} + \mathrm{He} \rightarrow")
        self.assertEqual(str(r2), "Ar+ + He →")
        self.assertEqual(r2.html, "Ar<sup>+</sup> + He →")
        self.assertEqual(r2.latex, r"\mathrm{Ar}^{+} + \mathrm{He} \rightarrow")

        r3 = Reaction("Kr+ + He+ -> Kr+2", strict=False)
        self.assertEqual(str(r3), "Kr+ + He+ → Kr+2")

    def test_species_aggregation(self):
        r = Reaction("2H + He + He -> H + H + 2He")
        reactants, products = r.reactants, r.products
        self.assertEqual([term[0] for term in reactants], [2, 1, 1])
        self.assertEqual([term[0] for term in products], [1, 1, 2])

    def test_reaction_equality(self):
        equal = [
            ["H + e- + H -> 2H + e-", "e- + 2H -> e- + 2H"],
            ["H + e+ + hv + H -> e+ + 2H + hv", "e+ + hv + 2H -> hv + e+ + 2H"],
            ["2H + He + He -> H + H + 2He", "2H + 2He -> 2H + He + He"],
            [
                "2H + He + He + hv -> H + hv + H + 2He",
                "2H + hv + 2He -> 2H + He + He + hv",
            ],
            ["H + H + M -> H2 + M", "2H + M -> H2 + M"],
            ["Kr + hv -> Kr + 2hv", "Kr + hv -> Kr + hv + hv"],
            ["Kr + hv -> Kr *", "Kr + hν -> Kr *"],
            ["Kr + e- -> Kr- *", "Kr + e -> Kr- *"],
        ]
        for r1, r2 in equal:
            self.assertEqual(Reaction(r1), Reaction(r2))

    def test_reaction_inequality(self):
        unequal = [
            ["H + He + H -> 2H + He", "He + 2H -> He + 2H"],
            ["H + He -> H+ + e- + He", "He + H -> H+ + e- + He"],
            ["He + He+ -> He+ + He", "He+ + He -> He + He+"],
        ]
        for r1, r2 in unequal:
            self.assertNotEqual(Reaction(r1), Reaction(r2))

    def test_reaction_str(self):
        for r_str in self.r_strings:
            with self.subTest(r_str):
                self.assertEqual(
                    str(Reaction(r_str)),
                    r_str.replace("<->", "⇌").replace("->", "→").replace("hv", "hν"),
                )

        s_r = "2H + M → H2 + M"
        r = Reaction(s_r)
        self.assertEqual(str(r), s_r)
        self.assertEqual(repr(r), "H + H + M → H2 + M")

    def test_reaction_html(self):
        for r_str, r_html in zip(self.r_strings, self.expected_html):
            with self.subTest(r_str):
                self.assertEqual(Reaction(r_str).html, r_html)

    def test_reaction_latex(self):
        for r_str, r_html in zip(self.r_strings, self.expected_latex):
            with self.subTest(r_str):
                self.assertEqual(Reaction(r_str).latex, r_html)

    def test_reaction_repr(self):
        for r_str, r_html in zip(self.r_strings, self.expected_repr):
            with self.subTest(r_str):
                self.assertEqual(repr(Reaction(r_str)), r_html)
        self.assertEqual(repr(Reaction("hv + C2 -> C + C")), "hν + C2 → C + C")
        self.assertEqual(repr(Reaction("e- + C2 -> C- + C")), "e- + C2 → C- + C")
        self.assertEqual(
            repr(Reaction("e- + C2 + e- -> C- + C-")), "2e- + C2 → C- + C-"
        )

    def test_reaction_m(self):
        s_r1 = "H + M -> H+ + e- + M"
        r = Reaction(s_r1)
        self.assertTrue(r.charge_conserved())
        self.assertTrue(r.stoichiometry_conserved())

    def test_reaction_species_map(self):
        r = Reaction("e- + C2 + e- -> C- + C-")
        self.assertEqual(r.reactants_text_count_map, {"e-": 2, "C2": 1})
        self.assertEqual(r.products_text_count_map, {"C-": 2})
        r = Reaction("e- + e- + hv -> ", strict=False)
        self.assertEqual(r.reactants_text_count_map, {"e-": 2, "hν": 1})
        self.assertEqual(r.products_text_count_map, {})
        r = Reaction("1e- + 1e- + 2hv -> ", strict=False)
        self.assertEqual(r.reactants_text_count_map, {"e-": 2, "hν": 2})
        r = Reaction("e- + O2 X(3Σ-g) -> ", strict=False)
        self.assertEqual(r.reactants_text_count_map, {"e-": 1, "O2 X(3Σ-g)": 1})
        r = Reaction("e- + O2 X(3SIGMA-g) -> ", strict=False)
        self.assertEqual(r.reactants_text_count_map, {"e-": 1, "O2 X(3Σ-g)": 1})

    def test_reaction_with_e(self):
        r = Reaction("e + C2 + e -> C- + C-")
        self.assertEqual(r.reactants_text_count_map, {"e-": 2, "C2": 1})
        self.assertEqual(r.products_text_count_map, {"C-": 2})
        self.assertEqual(repr(r), "2e- + C2 → C- + C-")


if __name__ == "__main__":
    unittest.main()
