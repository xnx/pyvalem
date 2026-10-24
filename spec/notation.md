# The PyValem notation

**Version 1.0, draft.** Implemented by PyValem 3.0.

The PyValem notation is a plain-text notation for the chemical formulas, quantum
states and reactions of atoms, ions and small molecules, of the kind recorded in
databases of atomic and molecular data. This document defines it so that it can
be implemented in any language. PyValem, the Python package, is the reference
implementation.

The test vectors in [`tests/`](tests/) are part of this specification: an
implementation conforms if it gives the results they record (section 8).

Contents:

1. [Conventions](#1-conventions)
2. [Characters](#2-characters)
3. [Numbers](#3-numbers)
4. [Formulas](#4-formulas)
5. [States](#5-states)
6. [Stateful species](#6-stateful-species)
7. [Reactions](#7-reactions)
8. [Conformance](#8-conformance)
9. [Tables](#9-tables)


## 1. Conventions

The key words MUST, MUST NOT, SHOULD and MAY are to be interpreted as described
in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

### Grammars

The grammars are parsing expression grammars
([PEG](https://bford.info/pub/lang/peg.pdf)). A rule `A <- e` defines `A` as the
expression `e`, built from:

| Expression | Meaning |
|---|---|
| `"text"` | the characters `text` |
| `[a-z]` | one character from the class |
| `e1 e2` | `e1` followed by `e2` |
| `e1 / e2` | `e1` if it matches, otherwise `e2` |
| `e?`, `e*`, `e+` | `e` zero or one times, zero or more times, one or more times |
| `&e`, `!e` | succeeds if `e` matches here (or doesn't), consuming nothing |
| `.`, `!.` | any one character; the end of the string |

Unlike the alternatives of a context-free grammar, choice is ordered and
repetition is greedy: `e*` takes as many repetitions as it can and never gives
any back. So each string has at most one parse, and the grammar says which. A
grammar must match the whole string, which the `!.` at the end of each top-level
rule makes explicit.

None of the grammars is recursive, so each defines a regular language. Some
rules can't conveniently be written in the grammar, and are given as numbered
constraints, such as F1. A string that breaks a constraint has invalid syntax.

### Errors

A string that is not valid notation has one of two kinds of error:

- a **syntax error**, if it doesn't match the grammar or breaks a constraint;
- a **validation error**, if it matches but describes something that can't
  exist, such as a term symbol whose J breaks the triangle rule.

An implementation MUST distinguish the two for states, because the
classification of states depends on it (section 5.1), and SHOULD distinguish
them for formulas.

### Canonical forms

Every formula, state, stateful species and reaction has a *canonical form*: a
string that is the same for everything that means the same thing, however it
was written. Two of them are equal if and only if their canonical forms are
equal. Parsing a canonical form MUST give something equal to what it came from,
and the canonical form of that MUST be the same string.


## 2. Characters

Strings are sequences of Unicode code points. These are the only non-ASCII
characters the notation uses:

| Character | Code point | Used for |
|---|---|---|
| `·` | U+00B7 MIDDLE DOT | a radical |
| `±` | U+00B1 PLUS-MINUS SIGN | the `(±)` formula prefix |
| `α β γ` | U+03B1, U+03B2, U+03B3 | formula prefixes |
| `Δ Λ` | U+0394, U+039B | formula prefixes; Δ also a molecular irrep |
| `ν` | U+03BD GREEK SMALL LETTER NU | the photon `hν`; vibrational states |
| `σ π δ` | U+03C3, U+03C0, U+03B4 | molecular orbitals |
| `Σ Π Φ Γ` | U+03A3, U+03A0, U+03A6, U+0393 | molecular irreps, with `Δ` |
| `→` | U+2192 RIGHTWARDS ARROW | reactions |
| `⇌` | U+21CC RIGHTWARDS HARPOON OVER LEFTWARDS HARPOON | reactions |
| combining tilde | U+0303 | molecular term labels |
| combining macron | U+0304 | molecular term labels |

No other character is equivalent to one of these. In particular, U+2206
INCREMENT is not `Δ`, U+2212 MINUS SIGN is not `-`, and U+2022 BULLET is not
`·`. The one exception is molecular term labels, which are normalised to Unicode
Normalization Form D first (section 5.8).

A formula or a state contains no whitespace.


## 3. Numbers

```peg
Count <- [1-9] [0-9]*            # a positive integer
UInt  <- "0" / [1-9] [0-9]*      # a non-negative integer
Half  <- UInt "/2"?              # an integer, n, or a half-integer, n/2
```

No number has a leading zero.

An angular momentum written as a `Half` has the value of the integer, or half
of it with `/2`. In a canonical form it is written as an integer if it is one,
and otherwise as `n/2` with `n` odd: `4/2` is written `2`.


## 4. Formulas

A formula describes an atom, isotope, ion, molecule or molecular ion, or one of
four special species. For example: `H2O`, `(13C)O2`, `Co(H2O)6+2`,
`CuSO4.5H2O`, `cis-1,2-CHFCHF`, `C2H5·` and `e-`.

### 4.1 Syntax

```peg
Formula     <- (Special / Prefixes? Moieties) !.
Special     <- ("e-" / "e+" / "e" / "hν" / "hv" / "M") !.
Prefixes    <- (Prefix "-")+ &Moiety
Prefix      <- Locants / Name
Locants     <- Count ("," Count)*
Name        <- # a prefix name from table 2, the longest that matches
Moieties    <- Moiety ("."? Moiety)* Charge?
Moiety      <- Unbracketed / Bracketed
Unbracketed <- CountOrX? Atoms Radical? Charge?
Bracketed   <- Count? "(" Atoms Radical? Charge? ")" CountOrX?
Atoms       <- (Atom CountOrX?)+
Atom        <- Element / Isotope / "D" / "T"
Isotope     <- "(" Count Element ")"
Element     <- # an element symbol from table 1, the longest that matches
CountOrX    <- Count / "x"
Charge      <- ("+" / "-") Count?
Radical     <- "·"
```

Constraints:

- **F1.** Only the last moiety may be unbracketed and have a charge: write
  `(NH3+)CH2CO2-`, not `NH3+CH2CO2-`.
- **F2.** A charge after the last moiety (the optional `Charge` of `Moieties`)
  is allowed only if that moiety is bracketed, and then no moiety may have a
  charge of its own: `(H2O)2+` and `Fe(CN)6-3` are valid, but `Li+2-` and
  `(H2O+)2+` are not.
- **F3.** One `Locants` prefix may not immediately follow another: write
  `1,1-`, not `1-1-`.

Some consequences of the grammar:

- Element symbols are tried before `D` and `T`, so `Dy`, `Ds` and `Ti` are
  elements, and `DsD` is darmstadtium deuteride.
- A prefix must be followed by a moiety, so `D-` is the deuteride ion and
  `D-H` is hydrogen with the `D` prefix.
- Digits after an atom are its count, so `SiO22H2O` is Si, O22, H2 and O. A
  period starts a moiety that has a multiplier: `SiO2.2H2O`.

### 4.2 Validation

- **V1.** An isotope must be one in the table of isotopes (section 9).
- **V2.** A moiety with a charge of its own must not have the count `x`, since
  its charge would be undefined: `(NH4+)x` is invalid.

### 4.3 Meaning

An `Element` is an atom with the natural isotopic composition; an `Isotope`,
such as `(13C)`, is an atom with the given mass number. `D` is `(2H)` and `T` is
`(3H)`.

The count after an atom multiplies it, and the count before an unbracketed
moiety multiplies the whole moiety. A bracketed moiety is multiplied by the
count before it and by the count after it. The count `x` is unspecified, as in
`CFx` or `CuSO4.xH2O`.

A charge of `+` or `-` is 1 or −1, and `+n` or `-n` is n or −n. A moiety's
charge is multiplied by the moiety's count. The charge of the formula is the
charge after the last moiety if there is one (F2), and otherwise the sum of the
charges of the moieties.

A radical dot and the prefixes don't change the composition.

The special species are the electron `e-` (which may be written `e`), the
positron `e+`, the photon `hν` (which may be written `hv`) and `M`, an
unspecified third body in a reaction.

### 4.4 Properties

An implementation SHOULD provide these properties of a formula:

- **Atom counts**: the number of each atom, keyed by element symbol for an
  element and by mass number and symbol for an isotope (`13C`, and `2H` for
  `D`), over all the moieties. A count is unspecified if any count that
  contributes to it is `x`.
- **Number of atoms**: the sum of the atom counts, unspecified if any of them
  is.
- **Charge**, as in section 4.3.
- **Mass**, in daltons: the sum of each atom's count times its mass, which is
  the standard atomic weight of an element or the atomic mass of an isotope
  (section 9). It is unspecified if any count is, or if an element has no
  standard atomic weight (such as Tc). The mass of an ion is the sum of the
  masses of its atoms, with no correction for its electrons.

The special species have no atoms. The electron and the positron have the
charges −1 and +1, and a mass of 5.48579909 × 10⁻⁴ Da; the photon has a
charge and mass of 0; and `M` has neither a charge nor a mass.

A *stoichiometric formula* lists each atom with its count (omitted if 1, and
`x` if unspecified), followed by the charge as in the canonical form. The atoms
are in one of three orders, in each of which an element comes before its
isotopes, which are in order of mass number:

- by atomic number: `H4C` for methane;
- alphabetically by element symbol: `CH4`;
- in Hill order: carbon, then hydrogen, then the other elements alphabetically,
  if the formula contains carbon, and otherwise alphabetically: `CH4`, `ClH`.

The stoichiometric formula of a special species is its canonical form.

### 4.5 Canonical form

The canonical form of a special species is `e-`, `e+`, `hν` or `M`. That of
any other formula is the formula as written, except that a count of 1 is
omitted and a charge of 1 is written `+` or `-`: `H1`, `1H2O`, `(OH)1` and
`H+1` become `H`, `H2O`, `(OH)` and `H+`. Everything else is kept as written,
including the order of the atoms, brackets and periods, and `D` and `T` (so `D`
and `(2H)` are different formulas).

### 4.6 HTML, LaTeX and slugs

These forms are informative: the test vectors give the forms PyValem produces,
which other implementations SHOULD match if they produce them.

- **HTML**: counts are subscripts, mass numbers are superscripts before the
  symbol, and charges are superscripts with the number before the sign:
  `Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>`. A radical is `&#183;` after
  the atoms. A multiplier is written before its moiety, and periods are
  omitted. The `D` and `L` prefixes are in small capitals, written
  `<span style="font-size: 80%;">D</span>`.
- **LaTeX** (for math mode): each symbol is `\mathrm{X}`, an isotope is
  `{}^{13}\mathrm{C}`, counts are `_{2}`, charges `^{2+}`, a radical is
  `\cdot`, and the prefixes `(±)`, `Δ`, `Λ`, `α`, `β` and `γ` are `(\pm)`,
  `\Delta`, `\Lambda`, `\alpha`, `\beta` and `\gamma`.
- **Slug**: a URL-safe string from which the formula can be recovered, such as
  `Co-_l_H2O_r_6_p2` for `Co(H2O)6+2`.


## 5. States

A state describes a quantum state or a label of a species, such as an
electronic configuration, a term symbol or a vibrational quantum number. There
are twelve types:

| Type | Examples | Section |
|---|---|---|
| Generic excited state | `*`, `**`, `3*` | 5.2 |
| Vibrational state | `v=2`, `2ν1+ν3` | 5.3 |
| Atomic configuration | `1s2.2s2.2p6`, `[Ne].3s` | 5.4 |
| Compound LS coupling | `4f(2Fo)5d` | 5.5 |
| Atomic term symbol | `2P_1/2`, `a5D` | 5.6 |
| Diatomic molecular configuration | `1σg2.1σu1` | 5.7 |
| Molecular term symbol | `X(1Σ+g)`, `A(1B2)` | 5.8 |
| J1K coupling | `2[9/2]_5` | 5.9 |
| J1J2 coupling | `(3/2,1/2)_2` | 5.10 |
| Rotational state | `J=5/2` | 5.11 |
| Racah symbol | `5p'[1/2]_1` | 5.12 |
| Key-value pair | `n=3` | 5.13 |

### 5.1 Classification

The type of a state is decided by its syntax:

1. If the state is `key=value` (split at the first `=`) with the key `J`, it is
   a rotational state, and if the key is `v` or `ν`, it is a vibrational state.
   It is an error if the state isn't valid as that type.
2. Otherwise, the types are tried in the order of the table above. If the state
   matches the syntax of a type, it is of that type, and a validation error is
   an error of the state: the later types are not tried.
3. If it matches none of them, it has a syntax error.

So, for example, `**` is a generic excited state, `2v1` is a vibrational state
rather than an atomic orbital (since `v` is also an orbital letter), `1G` is an
atomic term symbol rather than a molecular one, and `J=1/3` is an invalid
rotational state rather than a key-value pair.

### 5.2 Generic excited states

```peg
GenericExcited <- ("****" / "***" / "**" / "*" / UInt "*") !.
```

An unspecified excitation, as of a species to an unspecified level, or of an
ensemble to a range of levels. `n*` is the same as `n` asterisks, for n up to
4.

Canonical form: `*`, `**`, `3*`, `4*`, or `n*` for other n.

### 5.3 Vibrational states

```peg
Vibrational <- ("v=" / "ν=") (UInt / Unspecified) !.
             / Unspecified !.
             / Mode ("+" Mode)* !.
Unspecified <- "***" / "**" / "*"
Mode        <- UInt? ("v" / "ν") UInt
```

The vibrational quantum number of a diatomic molecule (`v=2`; `ν=2` is the
same), an unspecified vibrational excitation, or the number of quanta in each
of the normal modes of a polyatomic molecule: `2ν1+ν3` has two quanta in mode 1
and one in mode 3. A mode without a number of quanta has one.

Validation: a mode appears at most once.

Canonical form: `v=n`, `v=*`, `v=**` or `v=***`; or the modes in order of
mode number, each written `nνm` with `n` omitted if it is 1, joined by `+`.

### 5.4 Atomic configurations

```peg
AtomicConfig  <- (NobleGas / Orbital) ("." Orbital)* !.
NobleGas      <- "[He]" / "[Ne]" / "[Ar]" / "[Kr]" / "[Xe]" / "[Rn]"
Orbital       <- (UInt / "n") OrbitalLetter UInt?
OrbitalLetter <- [spdfghiklmnoqrtuvwxyz]
```

A sequence of occupied orbitals, each with its principal quantum number n (or
`n` if it is unspecified), its orbital letter (table 3) and its number of
electrons (1 if omitted). A noble gas in brackets stands for its closed-shell
configuration (table 5).

Validation: l < n (when n is given); an orbital has at most 2(2l + 1)
electrons; and no subshell (n and l) appears more than once, including those of
a noble-gas core.

Canonical form: all the orbitals, including those of a noble-gas core, in order
of n and then l, with those with an unspecified n last; each is written `nlk`,
with the number of electrons `k` omitted if it is 1; and they are joined by `.`.
So `[Ar].4s2.3d10` and `[Ar].3d10.4s2` have the same canonical form.

### 5.5 Compound LS coupling

```peg
CompoundLS <- (AtomicConfig "(" AtomicTerm ")")+ AtomicConfig? !.
```

Here `AtomicConfig` and `AtomicTerm` are the rules of sections 5.4 and 5.6
without their `!.`. A state of a complex atom in which groups of electrons are
LS-coupled to the intermediate terms in parentheses, as in `4f(2Fo)5d2(1G)`;
the final term is given as a separate atomic term symbol.

Validation: each configuration and term is valid. The state has a syntax error,
rather than a validation error, if any part has invalid syntax.

Canonical form: each configuration and term in its canonical form.

### 5.6 Atomic term symbols

```peg
AtomicTerm <- MooreLabel? UInt LLetter "o"? ("{" UInt "}")? ("_" Half)? !.
MooreLabel <- [a-z]
LLetter    <- [SPDFGHIKLMNOQRTUVWXYZ]
```

An LS-coupling term symbol: the spin multiplicity 2S + 1, the total orbital
angular momentum L as a letter (table 3), `o` for odd parity, a seniority in
braces, and the total angular momentum J. The optional lowercase letter before
it is a label of the kind used by C. E. Moore to distinguish terms with the
same S and L.

Validation: 2S + 1 ≥ 1; J − S is an integer; and |L − S| ≤ J ≤ L + S.

Canonical form: as written, with J in canonical form.

### 5.7 Diatomic molecular configurations

```peg
DiatomicConfig <- MO ("." MO)* !. / AltMO ("." AltMO)* !.
MO             <- UInt MOSymbol UInt?
AltMO          <- UInt OrbitalLetter "-" MOSymbol UInt?
MOSymbol       <- ("σ" / "π" / "δ" / "sigma" / "pi" / "delta") ("g" / "u")?
```

A sequence of occupied molecular orbitals, each with its counting number, its
symmetry and its number of electrons (1 if omitted). In the alternative
notation, such as `1s-σg2`, each orbital is labelled by the atomic orbital it
correlates with.

Validation: a σ orbital has at most 2 electrons and a π or δ orbital at most
4; and no orbital appears more than once.

Canonical form: the orbitals as written, with `σ`, `π` and `δ` for `sigma`,
`pi` and `delta`, and the number of electrons always written: `1sigmag` is
`1σg1`.

### 5.8 Molecular term symbols

```peg
MolecularTerm <- UInt "(" Term ")" !.
               / Label? ("(" Term ")" / Term) !.
Term          <- UInt Irrep ("_" ("+" / "-")? Half)?
Label         <- (Letter Diacritic?)+ ("'" / "\"")?
Letter        <- [A-Za-z]
Diacritic     <- "̃" / "̄"
Irrep         <- # an irreducible representation from table 4, the longest that matches
```

The state is first put in Unicode Normalization Form D, so that a precomposed
letter such as `Ã` is a letter followed by a combining tilde.

A molecular term symbol: the spin multiplicity 2S + 1, the irreducible
representation of the electronic wavefunction, and the projection Ω of the
total angular momentum. It may have a label before it, such as `X`, `A'`, `X̃`
or `EF`, or a number, which must be followed by the term in parentheses, as in
`1(2B1)`. The irreducible representations Σ, Π, Δ, Φ and Γ may be written
`SIGMA`, `PI`, `DELTA`, `PHI` and `GAMMA`.

Validation: 2S + 1 ≥ 1.

Canonical form: the label, if there is one, followed by the term in
parentheses; or the term alone. The term is written with Greek letters for the
irreducible representations of linear molecules, and Ω in canonical form
without a `+`. A term whose irreducible representation is a bare `G`, `H` or
`T` keeps its parentheses, without which it would be an atomic term symbol
(section 5.1): `(1G)`. A label's diacritics are combining characters.

### 5.9 J1K coupling

```peg
J1K <- UInt "[" Half "]" "o"? ("_" Half)? !.
```

A state in J1K (or LK) coupling, written as the multiplicity 2S + 1 of the
outer electron's spin, the angular momentum K in brackets, `o` for odd parity,
and the total angular momentum J.

Validation: 2S + 1 ≥ 1; J − S − K is an integer; and |K − S| ≤ J ≤ K + S.

Canonical form: K and J in canonical form.

### 5.10 J1J2 coupling

```peg
J1J2 <- "(" Half "," Half ")" "o"? ("_" Half)? !.
```

A state with two groups of electrons, each coupled to an angular momentum (J1
and J2), and perhaps to a total J.

Validation: J − J1 − J2 is an integer, and |J1 − J2| ≤ J ≤ J1 + J2.

Canonical form: the angular momenta in canonical form, with no space.

### 5.11 Rotational states

```peg
Rotational <- "J=" (UInt ("/2" / ".5" / ".0")? / "***" / "**" / "*") !.
```

The rotational quantum number J, or an unspecified rotational excitation. A
half-integer may also be written as a decimal (`J=1.5`), and so may an integer
(`J=1.0`).

Canonical form: `J=` followed by J in canonical form, or by the asterisks.

### 5.12 Racah symbols

```peg
Racah        <- UInt RacahOrbital "[" UInt "/" UInt "]" "o"? ("_" UInt)? !.
RacahOrbital <- ("s" / "p" / "d" / "f") "'"?
```

A state in Racah notation, as used for the excited states of the noble gases,
with an outer electron outside a p⁵ core: the electron's principal quantum
number and orbital letter, with a prime if the core's angular momentum is 1/2
rather than 3/2; the angular momentum K in brackets; `o` for odd parity; and
the total angular momentum J. The term symbol of the core is given as a
separate state.

Validation: K is a half-integer, written with the denominator 2; it couples
the core's angular momentum j and the electron's orbital angular momentum l,
|j − l| ≤ K ≤ j + l; and J is K + 1/2 or K − 1/2.

Canonical form: as written.

### 5.13 Key-value pairs

```peg
KeyValue <- Token "=" Token !.
Token    <- (!"=" !Space .)+
Space    <- # any whitespace character
```

An arbitrary quantum number or label, such as `n=3` or `sym=anti`. The keys
`J`, `v` and `ν` are reserved for rotational and vibrational states (section
5.1).

Canonical form: as written.


## 6. Stateful species

A stateful species is a formula, optionally followed by whitespace and a list
of states, as in `HCl v=2;J=0` or `Ar+ [Ne].3s2.3p5 2P_3/2`. The states are
separated by semicolons, by a comma followed by a space, or by whitespace, and
any number of these may separate two states. Each state is classified as in
section 5.1.

A species has at most one state of each type, except key-value pairs, of which
it may have several. They SHOULD have different keys.

The canonical form is the canonical form of the formula and, if there are any
states, a space and the canonical forms of the states, joined by `;`. The states
are sorted by the rank of their type and then, within a rank, by their
canonical form (comparing code points), except that key-value pairs are sorted
by key, with `n` first:

| Rank | Types |
|---|---|
| 0 | generic excited state |
| 1 | atomic configuration, compound LS coupling, diatomic molecular configuration |
| 2 | atomic term symbol, molecular term symbol |
| 3 | J1K coupling, J1J2 coupling |
| 4 | vibrational state |
| 5 | rotational state |
| 6 | Racah symbol |
| 7 | key-value pair |

So two stateful species are equal if they have the same formula and the same
states, in any order.


## 7. Reactions

A reaction is a list of reactants and a list of products, each species with a
coefficient, separated by one of the arrows ` → `, ` = `, ` ⇌ `, ` -> `,
` <-> ` and ` <=> `, which include the spaces around them. For example:
`2H2 + O2 → 2H2O` and `e- + Ar -> Ar+ + e- + e-`.

### 7.1 Parsing

A reaction string is parsed as follows:

1. If, without its trailing whitespace, it ends with an arrow (without the
   space after it), a space is added at the end; and if, without its leading
   whitespace, it starts with an arrow, a space is added at the start. (So a
   side may be empty.)
2. The arrows are tried in the order listed above, and the first that occurs in
   the string separates the reactants from the products. It is an error if no
   arrow occurs, or if that arrow occurs more than once.
3. Each side is split into terms at ` + `. Each term, without its surrounding
   whitespace, is ignored if it is empty, and is otherwise a coefficient and a
   stateful species. The coefficient is the digits at the start of the term,
   unless they are followed by a comma or a hyphen, when they are the locants
   of a prefix of the formula. A term without a coefficient has the
   coefficient 1. A coefficient MUST NOT start with 0.
4. It is an error if both sides are empty.

### 7.2 Validation

By default, a reaction MUST conserve atoms and charge:

- For each side, the atom counts of its species (section 4.4), times their
  coefficients, are summed, ignoring counts of 0. The two sums must be the
  same, where an unspecified count equals only another unspecified count.
- The charges of the species, times their coefficients, summed on each side,
  must be equal, ignoring `M`.

An implementation MAY offer to skip these checks, for incomplete reactions.

### 7.3 Canonical form

1. The light species, `e-`, `e+` and `hν`, are moved to the start of the
   reactants and to the end of the products. Among themselves, they are in the
   order `e+`, `e-`, `hν` among the reactants, and `hν`, `e-`, `e+` among the
   products. The other species stay in the order written.
2. Consecutive terms with the same light species are combined, adding their
   coefficients; any other term with the coefficient n becomes n terms with
   the coefficient 1.
3. Each term is its coefficient, if that isn't 1, and the canonical form of its
   species. A space separates the coefficient from a species that starts with a
   digit, as in `2 1,2-C2H4Cl2`.
4. The terms on each side are joined by ` + `, and the sides by ` → ` (for any
   of `→`, `=` and `->`) or ` ⇌ ` (for `⇌`, `<->` and `<=>`), with no space at
   the start or end.

So `C6H5OH + 7O2 → 6CO2 + 3H2O` has the canonical form
`C6H5OH + O2 + O2 + O2 + O2 + O2 + O2 + O2 → CO2 + CO2 + CO2 + CO2 + CO2 + CO2 + H2O + H2O + H2O`,
and `H + He -> H + He` is a different reaction from `He + H -> He + H`.


## 8. Conformance

The directory [`tests/`](tests/) has a JSON file of test vectors for each part
of the notation: `formulas.json`, `states.json`, `species.json` and
`reactions.json`. Each is an object whose `tests` member is a list of cases. A
case has an `input` string, and either an `error`, the kind of error the input
has, or the properties of what it describes, of which `canonical` is its
canonical form. The [README](README.md) describes the properties.

An implementation conforms to this specification if, for every case, it
reports the error given, or it accepts the input and gives the canonical form
and the other properties listed. Masses are equal if they agree to a relative
precision of 10⁻⁹.


## 9. Tables

**Table 1. Elements.** The element symbols are those of the 118 elements, H to
Og, in [`_data_atomic_weights.txt`](../src/pyvalem/_data_atomic_weights.txt),
which also gives their standard atomic weights. The isotopes and their atomic
masses are in
[`_data_isotope_masses.txt`](../src/pyvalem/_data_isotope_masses.txt).

**Table 2. Formula prefixes.** Locants, such as `1,2`, and these names:

`(+)` `(-)` `(±)` `D` `L` `(R)` `(S)` `(E)` `(Z)` `c` `l` `cis` `trans` `s`
`a` `Δ` `Λ` `α` `β` `γ` `n` `i` `t` `neo` `sec` `o` `m` `p` `ortho` `meta`
`para`

**Table 3. Angular momentum letters.** The orbital letters, for l = 0, 1,
2, …, are `s p d f g h i k l m n o q r t u v w x y z`, and the letters of L in
term symbols are the same in upper case: `S P D F G H I K L M N O Q R T U V W X
Y Z`. They skip `j`, and `p` and `s` after their first use.

**Table 4. Irreducible representations** in molecular term symbols:

- linear molecules: `Σ+` `Σ-` `Π` `Δ` `Φ` `Γ`, each with an optional `g` or
  `u` (`Σ+g`, `Πu`), where `Σ`, `Π`, `Δ`, `Φ` and `Γ` may be written `SIGMA`,
  `PI`, `DELTA`, `PHI` and `GAMMA`;
- other molecules: `A A' A" A1 A'1 A"1 A2 A'2 A"2 A3 Ag A'g A"g A1g A2g A3g Au
  A'u A"u A1u A2u A3u`, `B B' B" B1 B2 B3 Bg B'g B"g B1g B2g B3g Bu B'u B"u B1u
  B2u B3u`, `E E' E" E1 E'1 E"1 E2 E'2 E"2 E3 E'3 E"3 E4 E5 E6 E7 Eg E'g E"g
  E1g E2g E3g Eu E'u E"u E1u E2u E3u`, `T T1 T2 Tg T1g T2g Tu T1u T2u`, `G Gg
  Gu` and `H Hg Hu`.

**Table 5. Noble-gas cores.**

| Core | Configuration |
|---|---|
| `[He]` | `1s2` |
| `[Ne]` | `1s2.2s2.2p6` |
| `[Ar]` | `1s2.2s2.2p6.3s2.3p6` |
| `[Kr]` | `1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6` |
| `[Xe]` | `1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6.4d10.5s2.5p6` |
| `[Rn]` | `1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6.4d10.5s2.5p6.4f14.5d10.6s2.6p6` |
