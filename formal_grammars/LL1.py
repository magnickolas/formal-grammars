import tabulate

from .analyser_common import calc_follow
from .analyser_common import First
from .analyser_common import get_first
from .color import green
from .grammar import EMPTY
from .grammar import NonTerminals
from .grammar import Rules
from .grammar import Terminals


def main():
    Follow = calc_follow()

    M = [[""] * len(Terminals) for _ in range(len(NonTerminals))]

    for rule in Rules:
        A = rule.left
        A_idx = NonTerminals.index(A)
        first = get_first(rule.right)
        print(rule.right, first)
        for a in first.difference({EMPTY}):
            a_idx = Terminals.index(a)
            if M[A_idx][a_idx]:
                raise Exception("M already set")
            M[A_idx][a_idx] = rule
        if EMPTY in first:
            for b in Follow[A]:
                b_idx = Terminals.index(b)
                if M[A_idx][b_idx]:
                    raise Exception("M already set")
                M[A_idx][b_idx] = rule

    M_table = [[nonterm] + row for nonterm, row in zip(NonTerminals, M)]

    print(green("Terminals:"), "".join(Terminals))
    print(green("NonTerminals:"), "".join(NonTerminals))
    print()

    print(green("RULES"))
    for i, rule in enumerate(Rules):
        print(rule)
    print()

    print(green("FIRST"))
    for key, value in First.items():
        if key in NonTerminals:
            print(f"{key}: {{{', '.join(sorted(value))}}}")
    print()

    print(green("FOLLOW"))
    for key, value in Follow.items():
        if key in NonTerminals:
            print(f"{key}: {{{', '.join(sorted(value))}}}")
    print()

    print(green("M TABLE"))
    print(tabulate.tabulate(M_table, headers=[""] + Terminals, tablefmt="pipe"))
