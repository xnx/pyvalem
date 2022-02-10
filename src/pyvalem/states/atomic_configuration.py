"""Module with the `AtomicConfiguration` `State` subclass.

The `AtomicConfiguration` class, represents an atomic electronic configuration.
Methods are implemented for parsing a string into quantum numbers and
labels, creating an HTML representation of the term symbol, etc.
"""

import pyparsing as pp

from pyvalem.states._base_state import State, StateParseError

integer = pp.Word(pp.nums).setParseAction(lambda t: int(t[0]))
nocc_integer = pp.Optional(pp.Word(pp.nums), default="1").setParseAction(
    lambda t: int(t[0])
)

# NB no "j" orbital.
atomic_orbital_symbols = tuple("spdfghiklmnoqrtuvwxyz")
noble_gases = ["He", "Ne", "Ar", "Kr", "Xe", "Rn"]
noble_gas_configs = {
    "He": "1s2",
    "Ne": "[He].2s2.2p6",
    "Ar": "[Ne].3s2.3p6",
    "Kr": "[Ar].3d10.4s2.4p6",
    "Xe": "[Kr].4d10.5s2.5p6",
    "Rn": "[Xe].4f14.5d10.6s2.6p6",
}
noble_gas_nelectrons = {"He": 2, "Ne": 10, "Ar": 18, "Kr": 36, "Xe": 54, "Rn": 86}

noble_gas = pp.oneOf(["[{}]".format(symbol) for symbol in noble_gases])

atom_orbital = pp.Group(
    integer.setResultsName("n")
    + pp.oneOf(atomic_orbital_symbols).setResultsName("lletter")
    + nocc_integer.setResultsName("nocc")
)

atom_config = (
    (atom_orbital | noble_gas)
    + pp.ZeroOrMore(pp.Suppress(".") + atom_orbital).leaveWhitespace()
    + pp.StringEnd()
).leaveWhitespace()


class AtomicOrbitalError(StateParseError):
    pass


class AtomicConfigurationError(StateParseError):
    pass


class AtomicOrbital:
    # noinspection PyUnresolvedReferences
    """A class representing a single atomic orbital.

    This is a building block of the `AtomicConfiguration` state class.

    Parameters
    ----------
    n : int
        The principal quantum number.
    l : int, optional
        The azimuthal quantum number (0, 1, 2, ..., n-1)
        At least one of {`l`, `lletter`} must be passed.
    nocc : int, default: 1
        Number of occupied electrons.
    lletter : str, optional
        The letter corresponding to l: 's', 'p', 'd', ... for l = 0, 1, 2, ...
        At least one of {`l`, `lletter`} must be passed.

    Attributes
    ----------
    n : int
    l : int
    lletter : str
    html
    latex

    Raises
    ------
    AtomicOrbitalError
        If inconsistent quantum numbers are passed to the constructor.
    """

    def __init__(self, n, l=None, nocc=0, lletter=None):
        self.n = n
        if l is None:
            self.lletter = lletter
            try:
                self.l = atomic_orbital_symbols.index(lletter)
            except IndexError:
                raise AtomicOrbitalError(
                    "Invalid azimuthal quantum"
                    ' number label, lletter="{}"'.format(lletter)
                )
        else:
            self.l = l
            try:
                self.lletter = atomic_orbital_symbols[l]
            except IndexError:
                raise AtomicOrbitalError(
                    "Invalid azimuthal quantum"
                    " number, l={}. Must be in range 0 < l < {}".format(
                        l, len(atomic_orbital_symbols)
                    )
                )
            if lletter and lletter != self.lletter:
                raise AtomicOrbitalError(
                    "Inconsistent azimuthal quantum"
                    " number, l={} and label, lletter={} specified".format(l, lletter)
                )

        self.nocc = nocc
        self._validate_atomic_orbital()

    def __repr__(self):
        if self.nocc != 1:
            return "{}{}{}".format(self.n, self.lletter, self.nocc)
        return "{}{}".format(self.n, self.lletter)

    @property
    def html(self):
        """Html representation of the AtomicOrbital instance.

        Returns
        -------
        str
        """
        if self.nocc != 1:
            return "{}{}<sup>{}</sup>".format(self.n, self.lletter, self.nocc)
        return "{}{}".format(self.n, self.lletter)

    @property
    def latex(self):
        """LaTeX representation of the AtomicOrbital instance.

        Returns
        -------
        str
        """
        if self.nocc != 1:
            return "{}{}^{{{}}}".format(self.n, self.lletter, self.nocc)
        return "{}{}".format(self.n, self.lletter)

    def _validate_atomic_orbital(self):
        """Validator method for the atomic orbital class.

        Checks if the quantum numbers passed are consistent and physical and
        raises `AtomicOrbitalError` if not.

        Raises
        ------
        AtomicOrbitalError
        """
        if self.l > self.n - 1:
            raise AtomicOrbitalError("l >= n in atomic orbital {}".format(self))
        if self.nocc < 0:
            raise AtomicOrbitalError(
                "Negative nocc = {} not allowed in"
                " orbital: {}".format(self.nocc, self.nocc)
            )
        if self.nocc > 2 * (2 * self.l + 1):
            raise AtomicOrbitalError(
                "Too many electrons in atomic" " orbital: {}".format(self)
            )


class AtomicConfiguration(State):
    # noinspection PyUnresolvedReferences
    """A class representing an atomic configuration.

    An atomic configuration is considered as a collection of occupied atomic
    orbitals: e.g. 1s2.2s2.2p6.3s1; this may be abbreviated by using [X] where
    [X] is a noble gas atom as a short cut for the closed-shell configuration
    of X.

    Parameters
    ----------
    state_str : str
        State string in the required format

    Attributes
    ----------
    state_str : str
    orbitals : list of `AtomicOrbital`
        This list does *not* include the closed-shell nobel gas configuration.
    noble_gas_config : str or NoneType
        For example "[Ne]"
    nelectrons : int
        Number of electrons in the whole configuration.
    html
    latex

    Raises
    ------
    AtomicConfigurationError
        If the state cannot be parsed from the `state_str`.

    Notes
    -----
    The ``__repr__`` method is overloaded to provide a *canonicalised* representation
    of the state.
    The idea is that two states representing the same physical entity will have the
    same ``repr(state)`` representation.

    Examples
    --------
    >>> ac1 = AtomicConfiguration("1s2.2s2.2p6.3p1")
    >>> outer_orbital = ac1.orbitals[-1]
    >>> type(outer_orbital)
    <class 'pyvalem.states.atomic_configuration.AtomicOrbital'>

    >>> outer_orbital.n, outer_orbital.l, outer_orbital.nocc
    (3, 1, 1)

    >>> repr(ac1)
    '1s2.2s2.2p6.3p'

    >>> ac2 = AtomicConfiguration("[Ne].3p")
    >>> repr(ac2)
    '1s2.2s2.2p6.3p'
    """

    def __init__(self, state_str):
        self.state_str = state_str
        self.orbitals = []
        self.noble_gas_config = None
        self.nelectrons = 0
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        """Parses the `AtomicConfiguration` instance from the supplied `state_str`.

        Parameters
        ----------
        state_str : str

        Raises
        ------
        AtomicConfigurationError
            If the `state_str` cannot be parsed into a valid state.
        """
        try:
            parse_results = atom_config.parseString(state_str)
        except pp.ParseException:
            raise AtomicConfigurationError(
                "Invalid atomic electronic"
                " configuration syntax: {0}".format(state_str)
            )

        # Expand out noble gas notation, if used, and check that the
        # subshells 1s, 2s, 2p, ... are unique.
        subshells = self._expand_noble_gas_config(state_str)
        subshells = [subshell[:2] for subshell in subshells.split(".")]

        for i, parsed_orbital in enumerate(parse_results):
            if not i and type(parsed_orbital) == str:
                # Noble-gas notation for first atomic orbital
                self.noble_gas_config = parsed_orbital
                # NB strip '[' and ']' from parsed_orbital of the form '[Ar]'.
                self.nelectrons = noble_gas_nelectrons[parsed_orbital[1:-1]]
                continue
            # Create a validated AtomicOrbital object for this orbital.
            try:
                orbital = AtomicOrbital(
                    n=parsed_orbital["n"],
                    lletter=parsed_orbital["lletter"],
                    nocc=parsed_orbital["nocc"],
                )
                self.nelectrons += orbital.nocc
            except AtomicOrbitalError as err:
                raise AtomicConfigurationError(err)
            self.orbitals.append(orbital)

        # Check that the subshells specified are unique
        if len(subshells) != len(set(subshells)):
            raise AtomicConfigurationError("Repeated subshell in {0}".format(state_str))

    @property
    def html(self):
        """See the `State` base class."""
        html_chunks = []
        if self.noble_gas_config:
            html_chunks.append(self.noble_gas_config)
        for orbital in self.orbitals:
            html_chunks.append(orbital.html)
        return "".join(html_chunks)

    @property
    def latex(self):
        """See the `State` base class."""
        latex_chunks = []
        if self.noble_gas_config:
            latex_chunks.append(r"\mathrm{{{}}}".format(self.noble_gas_config))
        for orbital in self.orbitals:
            latex_chunks.append(orbital.latex)
        return "".join(latex_chunks)

    def _expand_noble_gas_config(self, config):
        """Recursively expand out the noble gas notation to orbitals.

        For example:
        '[He].2s1' -> '1s2.2s2',
        '[Xe].4f7' -> '1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6.4d10.5s2.5p6.4f7'

        Parameters
        ----------
        config : str
            Closed shell nobel gas configuration, in the form of '[Ne]', '[Xe]', etc.

        Returns
        -------
        str
        """

        if config[0] != "[":
            return config
        return (
            self._expand_noble_gas_config(noble_gas_configs[config[1:3]]) + config[4:]
        )

    def __repr__(self):
        """See the `State` base class."""
        if self.noble_gas_config:
            state_repr = self._expand_noble_gas_config(self.noble_gas_config)
            if self.orbitals:
                state_repr += "." + ".".join(repr(orbital) for orbital in self.orbitals)
            return state_repr
        else:
            return ".".join(repr(orbital) for orbital in self.orbitals)
