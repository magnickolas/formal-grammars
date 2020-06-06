# Cocke — Younger — Kasami algorithm
# for an arbitrary context-free grammar
from typing import Set

from tabulate import tabulate

from .color import green
from .color import yellow
from .grammar import EMPTY
from .grammar import NonTerminal
from .grammar import NonTerminals
from .grammar import Rules
from .grammar import START
from .grammar import Terminals


# Returns {A | A ⇒* ε}
def get_eps_closure() -> Set[NonTerminal]:
    C = set()
    for rule in Rules:
        if rule.right == EMPTY:
            C.add(rule.left)
    while True:
        changed = False
        for rule in Rules:
            if all(map(lambda X: X in C, rule.right)):
                A = rule.left
                if A not in C:
                    changed = True
                    C.add(A)
        if not changed:
            break
    return C


def calc_dp(word: str):
    n = len(word)
    # dp[A,i,j+1] = (A ⇒* word[i..j])
    # dp[A,i,i] = (A ⇒* ε)
    dp = {A: [[False] * (n + 1) for _ in range(n + 1)] for A in NonTerminals}
    # h[A→α,i,j+1,k] = (α[:k] ⇒* w[i..j])
    # h[A→α,i,i,k] = (α[:k] ⇒* ε)
    h = {
        rule: [
            [[False] * (len(rule.right) + 1) for _ in range(n + 1)] for _ in range(n)
        ]
        for rule in Rules
    }

    ## Base case
    for A in get_eps_closure():
        for i in range(n + 1):
            dp[A][i][i] = True
    for rule in Rules:
        A = rule.left
        α = rule.right
        if len(α) == 1:
            for i, _ in filter(lambda x: x[1] == α, enumerate(word)):
                dp[A][i][i + 1] = True
    for rule in Rules:
        for i in range(n):
            h[rule][i][i][0] = True

    ## Dynamics
    # h[A→α,i,j+1,k] = OR(h[A→α,i,r,k-1] && dp[α[k-1],r,j+1] foreach r=i..j+1)
    # dp[A,i,j] = OR(h[A→α,i,j,|α|] foreach A→α)
    for d in range(n + 1):
        for i in range(min(n, n - d + 1)):
            j = i + d - 1
            for _ in range(2):
                for rule in Rules:
                    A = rule.left
                    α = rule.right
                    for k in range(1, len(α) + 1):
                        c = α[k - 1]
                        for r in range(i, j + 2):
                            if h[rule][i][r][k - 1] and (
                                (r == j and c in Terminals and c == word[r])
                                or (c in NonTerminals and dp[c][r][j + 1])
                            ):
                                h[rule][i][j + 1][k] = True
                                break
                    if h[rule][i][j + 1][len(α)]:
                        dp[A][i][j + 1] = True
    return dp


def is_accepted(word: str) -> bool:
    dp = calc_dp(word)
    return dp[START][0][len(word)]


def main(args):
    word = args.word
    n = len(word)

    table = [[""] * n for _ in range(n)]

    dp = calc_dp(word)

    for d in range(n):
        for i in range(n - d):
            j = i + d
            for A in NonTerminals:
                if dp[A][i][j + 1]:
                    if A == START and d == n - 1:
                        # Highlight start symbol if it products the whole word
                        table[d][i] += yellow(A)
                    else:
                        table[d][i] += A

    print(green("CYK TABLE"))
    print("\n".join(str(tabulate(table, headers=word)).splitlines()[::-1]))
