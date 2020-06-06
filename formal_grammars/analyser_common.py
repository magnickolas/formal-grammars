from collections import defaultdict
from typing import Dict
from typing import Set
from typing import Union

from .grammar import EMPTY
from .grammar import LAST
from .grammar import NonTerminal
from .grammar import NonTerminals
from .grammar import Rules
from .grammar import RulesDict
from .grammar import START
from .grammar import Symbol
from .grammar import Terminal
from .grammar import Terminals


def calc_first_for_symbols() -> Dict[Symbol, Set[Union[Terminal, EMPTY]]]:
    first = defaultdict(set)
    first[EMPTY] = {EMPTY}
    for a in Terminals:
        first[a] = {a}
    while True:
        changed = False
        for rule in Rules:
            if rule.right == EMPTY:
                first[rule.left].add(EMPTY)
        for X in NonTerminals:
            for rule in RulesDict[X]:
                for Y in rule.right:
                    first[X].update(first[Y].difference({EMPTY}))
                    if EMPTY not in first[Y]:
                        break
                else:
                    if EMPTY not in first[X]:
                        changed = True
                    first[X].add(EMPTY)
        if not changed:
            break
    return first


First = calc_first_for_symbols()


def get_first(word: str) -> Set[Union[Terminal, EMPTY]]:
    first = set()
    for X in word:
        first.update(First[X].difference({EMPTY}))
        if EMPTY not in First[X]:
            break
    else:
        first.add(EMPTY)
    return first


def calc_follow() -> Dict[NonTerminal, Set[Terminal]]:
    follow = defaultdict(set)
    follow[START] = {LAST}
    for rule in Rules:
        for i in range(len(rule.right)):
            X = rule.right[i]
            if X in NonTerminals:
                follow[X].update(get_first(rule.right[i + 1 :]).difference({EMPTY}))
    while True:
        changed = False
        for rule in Rules:
            for i in range(len(rule.right)):
                X = rule.right[i]
                if X in NonTerminals:
                    if i == len(rule.right) - 1 or EMPTY in get_first(
                        rule.right[i + 1 :]
                    ):
                        follow[X].update(follow[rule.left])
        if not changed:
            break
    return follow
