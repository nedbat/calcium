import pprint
import sys
from pathlib import Path

from tokenizer import tokenize
from parser import Parser


def main(args):
    source = Path(args[0]).read_text()
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    pprint.pprint(ast)


if __name__ == "__main__":
    main(sys.argv[1:])
