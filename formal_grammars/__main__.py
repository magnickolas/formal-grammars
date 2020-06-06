from argparse import ArgumentParser

from . import CYK
from . import generate_words
from . import LL1
from . import LR1


def pname(parser):
    return dict(parser._get_kwargs())["prog"].split()[-1]


parser = ArgumentParser()
subparsers = parser.add_subparsers(dest="cmd", required=True)
parser_LL = subparsers.add_parser("ll1")
parser_LR = subparsers.add_parser("lr1")
parser_gen = subparsers.add_parser("gen")
parser_gen.add_argument("-n", "--num", type=int, default=20)
parser_cyk = subparsers.add_parser("cyk")
parser_cyk.add_argument("word", type=str)

args = parser.parse_args()

if args.cmd == pname(parser_LL):
    LL1.main()
elif args.cmd == pname(parser_LR):
    LR1.main()
elif args.cmd == pname(parser_gen):
    generate_words.main(args)
elif args.cmd == pname(parser_cyk):
    CYK.main(args)
