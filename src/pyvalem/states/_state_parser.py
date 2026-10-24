"""
A module for parsing strings or sequences of strings into appropriate
State-like objects or sequences of such objects.
"""

from collections import OrderedDict

from ._base_state import StateParseError, StateValidationError
from .atomic_configuration import AtomicConfiguration
from .atomic_term_symbol import AtomicTermSymbol
from .compound_LS_coupling import CompoundLSCoupling
from .diatomic_molecular_configuration import DiatomicMolecularConfiguration
from .generic_excited_state import GenericExcitedState
from .J1J2_coupling import J1J2_Coupling
from .J1K_LK_coupling import J1K_LK_Coupling
from .key_value_pair import KeyValuePair
from .molecular_term_symbol import MolecularTermSymbol
from .racah_symbol import RacahSymbol
from .rotational_state import RotationalState
from .vibrational_state import VibrationalState

# the following has two purposes: keys determine the order in which the
# states are parsed, and the values determine the sorting order of states
# for StatefulSpecies.__repr__.
STATES = OrderedDict(
    [
        (GenericExcitedState, 0),
        # NB before AtomicConfiguration, because v is also an atomic orbital
        # letter (l = 17): 2v1 is a vibrational state, not an invalid orbital.
        (VibrationalState, 4),
        (AtomicConfiguration, 1),
        (CompoundLSCoupling, 1),
        (AtomicTermSymbol, 2),
        (DiatomicMolecularConfiguration, 1),
        (MolecularTermSymbol, 2),
        (J1K_LK_Coupling, 3),
        (J1J2_Coupling, 3),
        (RotationalState, 5),
        (RacahSymbol, 6),
        (KeyValuePair, 7),
    ]
)

# The keys of key=value states whose values have their own syntax: such a state
# is never a generic KeyValuePair, so that, for example, J=1/3 is an error
# rather than an arbitrary label.
RESERVED_KEYS = {"J": RotationalState, "v": VibrationalState, "ν": VibrationalState}


def state_parser(s_state):
    """Parse s_state into an appropriate State-like object or list of such."""

    if not isinstance(s_state, str):
        # If we have a sequence of strings, parse them one by one into a list
        # of State-like objects.
        return [state_parser(s.strip()) for s in s_state]

    if not s_state:
        return None

    # A key=value state with a reserved key can only be of that key's type.
    key, sep, _ = s_state.partition("=")
    if sep and key in RESERVED_KEYS:
        return RESERVED_KEYS[key](s_state)

    # Try to parse the string s_state into a State-like object by trying each
    # of the possible derived State classes one by one in a particular order.
    # A StateValidationError means that s_state has the syntax of that type of
    # state but describes one that can't exist, so it is raised rather than
    # trying the other types.
    for StateClass in STATES:
        try:
            return StateClass(s_state)
        except StateValidationError:
            raise
        except StateParseError:
            pass

    raise StateParseError("Could not parse {}".format(s_state))
