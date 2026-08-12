import pprint
import sys
from pathlib import Path

from compiler import Compiler
from interpreter import CalcVm
from parser import Parser
from tokenizer import tokenize


def main(args):
    source = Path(args[0]).read_text()
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    print("\n=== AST =======================")
    pprint.pprint(ast)
    bytecode = Compiler(ast).compile()
    print("\n=== Byte code =================")
    for bc in bytecode:
        print(bc)
    print("\n=== Execute ===================")
    CalcVm().execute(bytecode)


if __name__ == "__main__":
    main(sys.argv[1:])
