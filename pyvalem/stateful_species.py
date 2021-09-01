"""
The StatefulSpecies class representing a chemical species (e.g. atom,
molecule), optionally with with one or more State objects associated with it.

The Formula of the StatefulSpecies is separated from its States by whitespace;
States are separated from each other by semicolons (;).
"""
from .formula import Formula, FormulaParseError
from .atomic_configuration import AtomicConfiguration
from .diatomic_molecular_configuration import DiatomicMolecularConfiguration
from .state_parser import state_parser

class StatefulSpeciesError(Exception):
    pass

class StatefulSpecies:

    def __init__(self, s):
        s = s.strip()
        if ' ' not in s:
            # No states, just a Formula
            self.states = []
            self.formula = Formula(s)
            return

        i = s.index(' ')
        self.formula = Formula(s[:i])
        self.states = state_parser(s[i+1:].split(';'))

        self.verify_states()

    def __repr__(self):
        """Return a canonical text representation of the StatefulSpecies."""
        if self.states:
            return '{} {}'.format(self.formula,
                                  ';'.join(map(repr, self.states)))
        return self.formula.__repr__()

    def __eq__(self, other):
        """
        Two StatefulSpecies are equal if they have the same Formula and the
        equal States (in any order).
        """

        return (self.formula == other.formula and
            set(self.states) == set(other.states))

    def __hash__(self):
        return hash(repr(self))

    def verify_states(self):
        """Check that multiple states are not given where this is not allowed.

        For example, a StatefulSpecies may not have two atomic configurations.

        """

        state_class_counts = {}
        for state in self.states:
            state_class_counts.setdefault(state.__class__, 0)
            state_class_counts[state.__class__] += 1

        for state_class in state_class_counts:
            if (not state_class.multiple_allowed and
                state_class_counts[state_class] > 1):
                raise StatefulSpeciesError('Multiple states of type {}'
                    ' specified for {}'.format(state_class.__name__, self))
        return True

    def verify_atomic_configuration(self):
        atomic_configurations = [s for s in self.states
                                    if s.__class__ == AtomicConfiguration]
        if len(atomic_configurations) != 1:
            raise StatefulSpeciesError('Multiple AtomicConfigurations'
                                ' specified for {}'.format(self))
        if not atomic_configurations:
            return True
        atomic_configuration = atomic_configurations[0]
        if self.formula.natoms != 1:
            return True

        atom = next(iter(self.formula.atoms))
        nelectrons = atom.Z - self.formula.charge
        if nelectrons != atomic_configuration.nelectrons:
            raise StatefulSpeciesError('Incorrect number of electrons for'
                    ' {} in atomic configuration {}'.format(self.formula,
                                                        atomic_configuration))
        return True


    def verify_diatomic_inversion_parity(self):
        if self.formula.natoms != 2:
            return True
        homonuclear_diatomic = len(self.formula.atoms) == 1
        diatomic_configurations = [s for s in self.states
                              if s.__class__ == DiatomicMolecularConfiguration]
        if not diatomic_configurations:
            return True
        if len(diatomic_configurations) != 1:
            raise StatefulSpeciesError('Multiple DiatomicConfigurations'
                                       ' specified for {}'.format(self))
        diatomic_configuration = diatomic_configurations[0]
        has_parity_label = all(orbital.symbol[-1] in 'gu'
                               for orbital in diatomic_configuration.orbitals)
        if has_parity_label == homonuclear_diatomic:
            return True
        s_homohetero = 'homo' if homonuclear_diatomic else 'hetero'
        raise StatefulSpeciesError('Incorrect use of inversion parity label'
                    ' (u/g) for {}nuclear diatomic {}'.format(s_homohetero,
                                                              self.formula))
        


    @property
    def html(self):
        if not self.states:
            return self.formula.html
        return '{} {}'.format(self.formula.html,
                              '; '.join(s.html for s in self.states))

    @property
    def latex(self):
        if not self.states:
            return self.formula.latex
        return '{} \; {}'.format(self.formula.latex,
                              '; \; '.join(s.latex for s in self.states))
