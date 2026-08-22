"""
The main program for Calcium.

This reads the source code, then runs it through the four phases: tokenize,
parse, compile to byte code, and execute byte code.
"""

import pprint
import sys
from pathlib import Path

from compiler import Compiler
from interpreter import CalcVm
from parser import Parser
from tokenizer import tokenize


def main(args):
    source = Path(args[0]).read_text()
    tokens = list(tokenize(source))

    print("\n=== Tokens ====================")
    for t in tokens:
        print(t, end="\n" if t.kind == "eol" else "; ")

    print("\n=== AST =======================")
    ast = Parser(tokens).parse()
    pprint.pprint(ast)

    print("\n=== Bytecode ==================")
    bytecode = Compiler(ast).compile()
    for bc in bytecode:
        print(bc)

    print("\n=== Execute ===================")
    CalcVm().execute(bytecode)


if __name__ == "__main__":
    main(sys.argv[1:])
