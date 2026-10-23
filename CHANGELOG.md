# Changelog

## 3.0.0 (unreleased)

### Changed

- Formulas are parsed strictly: whitespace, leading zeros and zero counts, an
  unbracketed charge before the end of the formula, and a separator (`.`) at
  the start or end are errors. A charge after a bracketed moiety at the end is
  the charge of the whole formula, so a moiety may no longer also have its own
  (`(H2O+)2+` was +1).
- The canonical form of a formula (`repr()` and the `formula` attribute) omits
  counts of 1 and writes charges of 1 as `+` and `-`, so `H+1` equals `H+`.
- An unknown isotope, and a charged moiety with an unspecified count, raise the
  new `FormulaValidationError`, a `FormulaParseError`.

### Fixed

- The HTML and LaTeX of a radical put the dot where it is written, after the
  atoms and before any charge: `(OH·)2` was rendered as `(OH)₂·`.

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
