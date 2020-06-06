from itertools import count
from itertools import islice
from itertools import product
from typing import Iterable

from .CYK import is_accepted
from .grammar import Terminals


def get_grammar_words() -> Iterable[str]:
    for n in count():
        for word in map(lambda x: "".join(x), product(Terminals, repeat=n)):
            if is_accepted(word):
                yield word


def main(args):
    for word in islice(get_grammar_words(), args.num):
        print(word)
