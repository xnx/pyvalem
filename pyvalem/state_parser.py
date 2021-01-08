"""
A module for parsing strings or sequences of strings into appropriate
State-like objects or sequences of such objects.
"""
from .state import StateParseError
from .generic_excited_state import GenericExcitedState
from .atomic_configuration import AtomicConfiguration
from .atomic_term_symbol import AtomicTermSymbol
from .diatomic_molecular_configuration import DiatomicMolecularConfiguration
from .molecular_term_symbol import MolecularTermSymbol
from .rotational_state import RotationalState
from .vibrational_state import VibrationalState
from .racah_symbol import RacahSymbol
from .key_value_pair import KeyValuePair

STATES = (
    GenericExcitedState, 
    AtomicConfiguration,
    AtomicTermSymbol,
    DiatomicMolecularConfiguration,
    MolecularTermSymbol,
    VibrationalState,
    RotationalState,
    RacahSymbol,
#    PhaseState,
#    EnergyFreqWvln,
    KeyValuePair,
)

def state_parser(s_state):
    """Parse s_state into an appropriate State-like object or list of such."""

    if not s_state:
        return None

    if not isinstance(s_state, str):
        # If we have a sequence of strings, parse them one by one into a list
        # of State-like objects.
        return [state_parser(s.strip()) for s in s_state] 

    state = None
    # Try to parse the string s_state into a State-like object by trying each
    # of the possible derived State classes one by one in a particular order.
    for StateClass in STATES:
         try:
            return StateClass(s_state)
         except StateParseError:
            pass
        
    raise StateParseError('Could not parse {}'.format(s_state))
