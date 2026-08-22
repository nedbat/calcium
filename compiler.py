"""
The compiler walks the tree of AST nodes, writing bytecode to represent the
execution. The bytecodes will be executed by the interpreter.
"""

from typing import Any

from bytecodes import ByteCode, Op
from parser import Assign, BinOp, Int, Print, Program, Var


class Compiler:
    def __init__(self, program: Program) -> None:
        self.program = program
        self.bytecode: list[ByteCode] = []

    def add_bytecode(self, op: Op, val: Any) -> None:
        """Simple helper to add a bytecode to the growing program."""
        self.bytecode.append(ByteCode(op, val))

    def compile(self):
        """Main compiler."""
        for stmt in self.program.stmts:
            match stmt:
                case Assign(var_name, expr):
                    self.compile_expr(expr)
                    self.add_bytecode(Op.STORE_VAR, var_name)

                case Print(expr):
                    self.compile_expr(expr)
                    self.add_bytecode(Op.PRINT, None)

        return self.bytecode

    def compile_expr(self, expr):
        """Add bytecodes to calculate an expression."""
        match expr:
            case Int(value):
                self.add_bytecode(Op.PUSH_INT, value)

            case Var(var_name):
                self.add_bytecode(Op.LOAD_VAR, var_name)

            case BinOp(op, left, right):
                self.compile_expr(left)
                self.compile_expr(right)
                self.add_bytecode(Op.BIN_OP, op)
