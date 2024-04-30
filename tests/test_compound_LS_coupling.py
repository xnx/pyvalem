"""
Unit tests for the Compound LS Coupling module of PyValem
"""

import unittest

from pyvalem.states.atomic_configuration import AtomicConfiguration
from pyvalem.states.atomic_term_symbol import AtomicTermSymbol
from pyvalem.states.compound_LS_coupling import CompoundLSCoupling


class CompoundLSCouplingTest(unittest.TestCase):
    def test_compound_LS_coupling(self):
        s0 = CompoundLSCoupling("3d10.4f7(8So)4p6.5d(9Do)6s(8Do)7s")
        a0 = AtomicConfiguration("3d10.4f7")
        a1 = AtomicConfiguration("4p6.5d")
        a2 = AtomicConfiguration("6s")
        a3 = AtomicConfiguration("7s")
        for i, ac in enumerate((a0, a1, a2, a3)):
            self.assertEqual(ac, s0.atomic_configurations[i])
        self.assertEqual(
            s0.html,
            """3d<sup>10</sup>4f<sup>7</sup>(<sup>8</sup>S<sup>o</sup>)4p<sup>6</sup>5d(<sup>9</sup>D<sup>o</sup>)6s(<sup>8</sup>D<sup>o</sup>)7s""",
        )
        self.assertEqual(
            s0.latex,
            r"3d^{10}4f^{7}({}^{8}\mathrm{S}^o)4p^{6}5d({}^{9}\mathrm{D}^o)6s({}^{8}\mathrm{D}^o)7s",
        )

        s1 = CompoundLSCoupling("4f10(3K{2})6s.6p(1Po)")
        t0 = AtomicTermSymbol("3K{2}")
        t1 = AtomicTermSymbol("1Po")
        for i, ts in enumerate((t0, t1)):
            self.assertEqual(ts, s1.terms[i])
        self.assertEqual(s1.terms[0].seniority, 2)
        self.assertEqual(
            s1.html,
            """4f<sup>10</sup>(<sup>3</sup>K2)6s6p(<sup>1</sup>P<sup>o</sup>)""",
        )
        self.assertEqual(
            s1.latex, r"4f^{10}({}^{3}\mathrm{K}2)6s6p({}^{1}\mathrm{P}^o)"
        )

        s2 = CompoundLSCoupling("4d9(2P)5d2(3Fo)")
        self.assertEqual(
            s2.html,
            """4d<sup>9</sup>(<sup>2</sup>P)5d<sup>2</sup>(<sup>3</sup>F<sup>o</sup>)""",
        )
        self.assertEqual(
            s2.latex, r"4d^{9}({}^{2}\mathrm{P})5d^{2}({}^{3}\mathrm{F}^o)"
        )

        s3 = CompoundLSCoupling("5p5(2Po_3/2)6d")
        self.assertEqual(
            s3.html, """5p<sup>5</sup>(<sup>2</sup>P<sup>o</sup><sub>3/2</sub>)6d"""
        )
