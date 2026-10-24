# Changelog

## 3.0.1 (unreleased)

### Added

- Examples, in `examples/` and in the documentation: checking a list of
  reactions before it goes into a database, and applying the selection rules
  for atomic transitions. The tests check what they print.

### Fixed

- The period of a formula such as `CuSO4.5H2O` is a centred dot in its HTML
  (`&#183;`) and LaTeX (`\cdot`). It was missing, as it had been before 3.0,
  and the specification and its test vectors are corrected to match.
- The specification said that a formula can always be recovered from its slug,
  but a period next to a bracket or after a radical isn't recorded:
  `Co.(H2O)6` and `Co(H2O)6` have the same slug.

## 3.0.0 (24 October 2026)

PyValem 3.0 implements the notation as it is now specified. Input that 2.10
deprecated is rejected, and the canonical forms (`repr()`) of formulas and
states have changed, as has the order of isotopes in stoichiometric formulas:
data keyed on either will need updating. Slugs are unchanged.

### Added

- A specification of the notation, independent of Python, in
  `spec/notation.md`, with test vectors in `spec/tests/` that PyValem's tests
  run and that other implementations can be checked against.

### Changed

- Formulas are parsed strictly: whitespace, leading zeros and zero counts, an
  unbracketed charge before the end of the formula, and a separator (`.`) at
  the start or end are errors. A charge after a bracketed moiety at the end is
  the charge of the whole formula, so a moiety may no longer also have its own
  (`(H2O+)2+` was +1).
- States are parsed strictly: whitespace, leading zeros, and a bare number for
  a vibrational state (`2` for `v=2`) are errors, and so are leading zeros in a
  reaction coefficient.
- The canonical form of a formula (`repr()` and the `formula` attribute) omits
  counts of 1 and writes charges of 1 as `+` and `-`, so `H+1` equals `H+`.
- An unknown isotope, and a charged moiety with an unspecified count, raise the
  new `FormulaValidationError`, a `FormulaParseError`.
- Every type of state has a canonical form (`repr()`), so that equivalent
  states compare equal. Angular momenta are written as integers or fractions
  with odd numerators (`3P_2/2` is `3P_1`, `J=4/2` is `J=2`). A molecular term
  symbol's label is followed by the term in parentheses (`X1Σ+` is `X(1Σ+)`),
  except that a bare G, H or T term keeps its parentheses (`(1G)`), without
  which it would be atomic. J1J2 states are written without a space. An atomic
  configuration lists all its orbitals, including any noble-gas core, by n and
  then l, so `[Ar].4s2.3d10` equals `[Ar].3d10.4s2`; its HTML and LaTeX keep
  the order as written.
- A molecular term symbol's label may have a tilde or a macron on its letters,
  as in `X̃(2A1)` and `HH̄(1Σ+g)`; a precomposed letter such as `Ã` is written
  as the letter and a combining character in the canonical form. In LaTeX they
  are `\tilde{X}` and `\bar{H}`.
- A vibrational state that lists a mode more than once (`ν1+ν1`) raises the new
  `VibrationalStateValidationError`.
- In stoichiometric formulas, isotopes are listed with their element, after the
  element itself. In alphabetical order every isotope used to come first (so
  DCl gave `(2H)Cl`, now `Cl(2H)`), and Hill order now treats isotopes of
  carbon and hydrogen as carbon and hydrogen (`(13C)H3Cl`, not `(13C)ClH3`).

### Fixed

- The HTML and LaTeX of a radical put the dot where it is written, after the
  atoms and before any charge: `(OH·)2` was rendered as `(OH)₂·`.
- A species with separators but no states after its formula, such as `H2O ;`,
  raised `TypeError`.
- A formula and its states may be separated by any whitespace: a tab wasn't
  accepted.
- A σg or σu orbital was allowed four electrons, like a π or δ orbital:
  `1σg3` was accepted.
- Deuterium after a formula prefix, as in `trans-D`, was taken to be the `D`
  prefix, so the formula was rejected.

## 2.10.0 (24 October 2026)

### Deprecated

The following input, which PyValem 3.0 will reject, now gives a
`PyValemDeprecationWarning`. That is a `FutureWarning`, so it is shown by default.

- Whitespace inside a formula or a state, as in `H2 O`, `Ca (OH)2`, `2 P_1/2`
  and `J = 2`. Spaces still separate the formula and states of a
  `StatefulSpecies`, and the terms of a reaction.
- An unbracketed charge before the end of a formula, as in `NH2+CH3CHO2-`:
  write `(NH2+)CH3CHO2-`.
- A bare number as a vibrational state, as in `CO 2`: write `CO v=2`.
- Leading zeros and zero counts, as in `H02`, `H0`, `Ar+02` and `v=007`, and
  leading zeros in a reaction coefficient, as in `02H -> H2`.

## 2.9.0 (24 October 2026)

PyValem now needs Python 3.11 or later and pyparsing 3.1 or later.

### Fixed

- Diatomic configurations in the alternative notation (`1s-σg2`) all compared
  equal, and equal diatomic configurations (`1σg2` and `1sigmag2`) had
  different hashes.
- Comparing a `Formula`, `StatefulSpecies` or diatomic configuration with an
  object of another type raised `AttributeError`, and `Reaction` was unhashable.
- Unspecified stoichiometries other than at the end of a formula, as in `CxH4`,
  `(CH2)x` and `CuSO4.xH2O`, raised `TypeError` or `ValueError`.
- Numeric locants after another prefix, as in `trans-2-C4H8`, were rejected.
- A formula that starts with a locant, such as `1,2-C2H4Cl2`, couldn't appear in
  a reaction.
- Atomic configurations with two orbitals with the same n of 10 or more
  (`10s2.10p1`) were rejected as repeating a subshell, and a closed-shell core
  that wasn't at the start of a configuration was mangled.
- `Formula("Tc(98Tc)").stoichiometric_formula()` raised `TypeError`.
- The special species (e-, e+, hν and M) shared their attributes between
  instances.
- The LaTeX for ⇌ was `\rightlefthooks`, which isn't a LaTeX command; it is now
  `\rightleftharpoons`. The `(±)` prefix lost its parentheses in LaTeX.
- `StatefulSpecies.verify_atomic_configuration()` failed for a species without
  an atomic configuration, and `verify_diatomic_inversion_parity()` accepted a
  heteronuclear diatomic with some orbitals labelled g or u.
- `CompoundLSCoupling.term_symbols` was always empty, and its errors had no
  message.
- `RacahSymbol` ignored anything after a valid symbol.
- A reaction with no reactants was only accepted if it began with a space, and
  spaces around a term could change its meaning.

### Changed

- A state with the syntax of a type of state that describes a state that can't
  exist is reported as such, with the reason (such as the triangle rule for J),
  instead of "Could not parse" or being taken as a different type of state.
  These errors derive from the new `StateValidationError`, which is a
  `StateParseError`.
- `J=…`, `v=…` and `ν=…` states are always rotational or vibrational states: an
  invalid value such as `J=1/3` or `v=1.5` is an error rather than a
  `KeyValuePair`. `J=1.0` is accepted as J=1, and `ν=1` as v=1.
- `18v1` and the like are vibrational states, not atomic orbitals with l = 17.
- These are now rejected: Racah symbols whose K or J can't arise from the core
  and the electron (`5p[3/4]`, `3p[3/2]_3`), molecular term symbols with
  unbalanced parentheses, a spin multiplicity of 0, key-value pairs with an
  empty key or value, vibrational quantum numbers with a sign (so `Ti +2` is an
  error, not neutral titanium in v=2) and reaction coefficients of 0.
- Every exception raised for invalid input derives from the new
  `pyvalem.PyValemError`, which is a `ValueError`. A non-string argument raises
  `TypeError`.
- `Formula`, `StatefulSpecies`, `Reaction`, their exceptions and `__version__`
  can be imported from `pyvalem` itself.
- The `atoms` of e-, e+ and hν is an empty set, as for other formulas, instead
  of an empty dict.
