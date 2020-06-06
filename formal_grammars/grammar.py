from collections import defaultdict
from collections import namedtuple
from typing import NewType
from typing import Union

import yaml

## TYPES


class Rule(namedtuple("Rule", ["left", "right"])):
    __slots__ = ()

    def __repr__(self):
        return f"{self.left} → {self.right}"


class Item(namedtuple("Item", ["left", "prefix", "suffix", "lookahead"])):
    __slots__ = ()

    def __repr__(self):
        return f"[{self.left}→{self.prefix}.{self.suffix}," f" {self.lookahead}]"


Terminal = NewType("Terminal", str)
NonTerminal = NewType("NonTerminal", str)
Symbol = Union[Terminal, NonTerminal]

## Parsing grammar description file

Grammar = yaml.load(open("grammar.yaml", "r"), yaml.Loader)


def parse_rules(s):
    left, right = map(lambda x: "".join(x.split()), s.split(RULE_SEPARATOR))
    right_parts = map(
        lambda x: "".join(x.split()), right.split(RULE_RIGHT_PARTS_SEPARATOR)
    )
    return [Rule(left=left, right=right) for right in right_parts]


EMPTY = Grammar["empty"]
LAST = "$"
EXT_START = "@"
START = Grammar["start"]
RULE_SEPARATOR = "->"
RULE_RIGHT_PARTS_SEPARATOR = "|"

# [@->.S, $]
StartItem = Item(left=EXT_START, prefix="", suffix=START, lookahead=LAST)

# [@->S., $]
LastItem = Item(left=EXT_START, prefix=START, suffix="", lookahead=LAST)

Rules = []
for raw_rules in Grammar["rules"]:
    Rules.extend(parse_rules(raw_rules))

ExtRules = [Rule(left=EXT_START, right=START)] + Rules

# Create a convenient view
RulesDict = defaultdict(list)
for rule in Rules:
    RulesDict[rule.left].append(rule)

# Parse symbols from the rules (already got rid of whitespaces and separators) as
#   upper case symbols -> non terminals
#   other symbols -> terminals
Terminals, NonTerminals = set(), set()
for rule in Rules[1:]:
    s = rule.left + rule.right
    Terminals.update(filter(lambda c: not c.isupper() and c != EMPTY, s))
    NonTerminals.update(filter(lambda c: c.isupper(), s))
# Add end marker as terminal symbols
Terminals = sorted(Terminals) + [LAST]
NonTerminals = sorted(NonTerminals)

Symbols = Terminals + NonTerminals
