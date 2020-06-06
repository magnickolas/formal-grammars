from typing import FrozenSet
from typing import List
from typing import Set

import tabulate

from .analyser_common import First
from .analyser_common import get_first
from .color import green
from .grammar import EMPTY
from .grammar import ExtRules
from .grammar import Item
from .grammar import LAST
from .grammar import LastItem
from .grammar import NonTerminals
from .grammar import Rule
from .grammar import Rules
from .grammar import RulesDict
from .grammar import StartItem
from .grammar import Symbol
from .grammar import Symbols
from .grammar import Terminals


def closure(Items: Set[Item]) -> FrozenSet[Item]:
    J = Items.copy()
    while True:
        new_items = set()
        for item in J:
            fst_sym = item.suffix[0] if item.suffix else None
            lookaheads = get_first(item.suffix[1:] + item.lookahead)
            for rule in RulesDict[fst_sym]:
                for b in lookaheads:
                    new_item = Item(
                        left=rule.left,
                        prefix="",
                        suffix=rule.right if rule.right != EMPTY else "",
                        lookahead=b,
                    )
                    if new_item not in J:
                        new_items.add(new_item)
        J.update(new_items)
        if not new_items:
            break
    return frozenset(J)


def goto(Items: Set[Item], X: Symbol) -> FrozenSet[Item]:
    J = set()
    for item in Items:
        fst_sym = item.suffix[0] if item.suffix else None
        if fst_sym == X:
            J.add(
                Item(
                    left=item.left,
                    prefix=item.prefix + fst_sym,
                    suffix=item.suffix[1:],
                    lookahead=item.lookahead,
                )
            )
    return closure(J)


def get_items_sets() -> List[FrozenSet[Item]]:
    I_0 = closure({StartItem})
    C = [I_0]
    while True:
        new_sets = set()
        for Items in C:
            for X in Symbols:
                J = goto(Items, X)
                if J and J not in C:
                    new_sets.add(J)
        C.extend(list(new_sets))
        if not new_sets:
            break
    return C


def main():
    items_sets = get_items_sets()
    num_states = len(items_sets)
    Action = [[""] * len(Terminals) for _ in range(num_states)]
    Goto = [[""] * len(NonTerminals) for _ in range(num_states)]

    for i, items_set in enumerate(items_sets):
        for X_idx, X in enumerate(NonTerminals):
            goto_items_set = goto(items_set, X)
            if goto_items_set in items_sets:
                j = items_sets.index(goto_items_set)
                if Goto[i][X_idx] and Goto[i][X_idx] != j:
                    raise Exception("goto already set")
                Goto[i][X_idx] = j

    for i, items_set in enumerate(items_sets):
        for a_idx, a in enumerate(Terminals):
            goto_items_set = goto(items_set, a)
            action = ""
            if goto_items_set in items_sets:
                j = items_sets.index(goto_items_set)
                action = f"S{j}"
            to_rotate_items = list(
                filter(lambda item: not item.suffix and item.lookahead == a, items_set)
            )
            if to_rotate_items:
                tritem = to_rotate_items[0]
                rule = Rule(
                    left=tritem.left, right=tritem.prefix if tritem.prefix else EMPTY
                )
                j = ExtRules.index(rule)
                if action:
                    raise Exception("action already set")
                action = f"R{j}"
            if Action[i][a_idx] and Action[i][a_idx] != action:
                raise Exception("action already set")
            Action[i][a_idx] = action
        if LastItem in items_set:
            Action[i][Terminals.index(LAST)] = "acc"

    Action_table = [[i] + row for i, row in enumerate(Action)]

    action_table_width = len(
        str(
            tabulate.tabulate(Action_table, headers=["Q"] + Terminals, tablefmt="pipe")
        ).splitlines()[0]
    )
    Full_table = [
        action_row + goto_row for action_row, goto_row in zip(Action_table, Goto)
    ]

    print(green("Terminals:"), "".join(Terminals))
    print(green("NonTerminals:"), "".join(NonTerminals))
    print()

    print(green("RULES"))
    for i, rule in enumerate(Rules):
        print(rule, f"({i+1})")

    print()

    print(green("FIRST"))
    for key, value in First.items():
        if key in NonTerminals:
            print(f"{key}: {{{', '.join(sorted(value))}}}")
    print()

    print(green("CANONICAL SYSTEM"))
    for i, items_set in enumerate(items_sets):
        print(f"{i}: {' '.join(map(str, items_set))}")

    print()
    print(green("Action".ljust(action_table_width) + "Goto"))
    print(
        tabulate.tabulate(
            Full_table, headers=["Q"] + Terminals + NonTerminals, tablefmt="pipe"
        )
    )
