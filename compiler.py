from dataclasses import dataclass
from typing import Any

from parser import Assign, BinOp, Int, Print, Program, Var


@dataclass
class ByteCode:
    op: str
    val: Any

    def __str__(self):
        if self.val is not None:
            return f"{self.op:10s} {self.val}"
        else:
            return self.op


class Compiler:
    def __init__(self, program: Program) -> None:
        self.program = program
        self.bytecode = []

    def compile(self):
        for stmt in self.program.stmts:
            match stmt:
                case Assign(var_name, expr):
                    self.compile_expr(expr)
                    self.bytecode.append(ByteCode("STORE_VAR", var_name))
                case Print(expr):
                    self.compile_expr(expr)
                    self.bytecode.append(ByteCode("PRINT", None))
        return self.bytecode

    def compile_expr(self, expr):
        match expr:
            case Int(value):
                self.bytecode.append(ByteCode("PUSH_INT", value))
            case Var(var_name):
                self.bytecode.append(ByteCode("LOAD_VAR", var_name))
            case BinOp(op, left, right):
                self.compile_expr(left)
                self.compile_expr(right)
                self.bytecode.append(ByteCode("BIN_OP", op))
