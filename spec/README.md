# The PyValem notation: specification and test vectors

[`notation.md`](notation.md) specifies the PyValem notation for chemical formulas,
quantum states, stateful species and reactions, so that it can be implemented in
languages other than Python. The test vectors in [`tests/`](tests/) are part of
the specification, and are what an implementation is checked against: PyValem's
own test suite runs them.

## Test vectors

Each file is a JSON object (in UTF-8, with non-ASCII characters unescaped) whose
`tests` member is a list of cases. Every case has an `input` string, and either an
`error` or the properties of what the input describes.

`error` is the kind of error the input has (section 1 of the specification):
`syntax` or `validation`, and for reactions also `stoichiometry` or `charge`, if
the reaction doesn't conserve atoms or charge. An error in one of the formulas or
states of a species or reaction is of the same kind; two states of the same type
in a species are a `validation` error.

The properties are:

| File | Properties |
|---|---|
| `formulas.json` | `canonical`; `charge` (`null` for `M`); `natoms` and `atoms`, the number of atoms and the count of each, keyed by element symbol or by mass number and symbol (`13C`), with `null` for an unspecified count; `mass` in daltons, or `null`; `stoichiometric`, the stoichiometric formulas in each order (`atomic number`, `alphabetical` and `hill`); and `html`, `latex` and `slug` |
| `states.json` | `type`, one of `GenericExcitedState`, `VibrationalState`, `AtomicConfiguration`, `CompoundLSCoupling`, `AtomicTermSymbol`, `DiatomicMolecularConfiguration`, `MolecularTermSymbol`, `J1K_LK_Coupling`, `J1J2_Coupling`, `RotationalState`, `RacahSymbol` and `KeyValuePair`; `canonical`; `html`; and `latex` |
| `species.json` | `canonical`; `formula`, the canonical form of the formula; `states`, each with its `type` and `canonical` form, in the order written; `html`; and `latex` |
| `reactions.json` | `canonical`; `reactants` and `products`, as `[coefficient, species]` pairs in the order written, with each species in canonical form; `html`; and `latex`. A case with `"strict": false` skips the checks of conservation (section 7.2). |

Masses agree if they are equal to a relative precision of 10⁻⁹. The `html`,
`latex` and `slug` forms are informative (section 4.6 of the specification).

Some molecular term symbols in `states.json` have labels with combining
characters, or with precomposed letters such as `Ã`, which look the same as the
decomposed form but aren't: their canonical forms are decomposed.
