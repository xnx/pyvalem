"""
Grammar rules shared by the parsers of formulas and states.
"""

import pyparsing as pp

# An unsigned integer, without leading zeros.
uint = pp.Regex(r"0|[1-9][0-9]*")
# A positive integer, without leading zeros.
count = pp.Regex(r"[1-9][0-9]*")
