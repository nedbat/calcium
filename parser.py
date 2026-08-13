from dataclasses import dataclass
from typing import Never

from tokenizer import Token


@dataclass
class Ast: ...


@dataclass
class Expr(Ast): ...


@dataclass
class Int(Expr):
    value: int


@dataclass
class Var(Expr):
    name: str


@dataclass
class BinOp(Expr):
    op: str
    left: Expr
    right: Expr


@dataclass
class Stmt(Ast): ...


@dataclass
class Assign(Stmt):
    var_name: str
    expr: Expr


@dataclass
class Print(Stmt):
    expr: Expr


@dataclass
class Program(Ast):
    stmts: list[Stmt]


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = iter(tokens)
        self.token = Token("eol", "")

    def error(self, msg=None) -> Never:
        if msg is None:
            msg = f"Didn't understand token {self.token.text}"
        raise RuntimeError(f"Error! {msg}")

    def eat(self) -> None:
        self.token = next(self.tokens, Token("eof", ""))

    def expect(self, text):
        if self.token.text == text:
            self.eat()
        else:
            self.error(f"Expected {text!r}")

    def expect_kind(self, kind):
        if self.token.kind == kind:
            self.eat()
        else:
            self.error(f"Expected {kind}")

    def parse(self) -> Program:
        stmts = []
        self.eat()
        while self.token.kind != "eof":
            if self.token.kind == "eol":
                self.eat()
                continue
            stmts.append(self.statement())
        return Program(stmts)

    def statement(self) -> Stmt:
        if self.token.kind == "nam":
            var_name = self.token.text
            self.eat()
            self.expect("=")
            expr = self.expression()
            stmt = Assign(var_name, expr)
        elif self.token.text == "print":
            self.eat()
            stmt = Print(self.expression())
        else:
            self.error()
        self.expect_kind("eol")
        return stmt

    def expression(self) -> Expr:
        return self.sum()

    def sum(self) -> Expr:
        expr = self.product()
        while self.token.text in {"+", "-"}:
            op = self.token.text
            self.eat()
            right = self.product()
            expr = BinOp(op, expr, right)
        return expr

    def product(self) -> Expr:
        expr = self.leaf()
        while self.token.text in {"*", "/"}:
            op = self.token.text
            self.eat()
            right = self.leaf()
            expr = BinOp(op, expr, right)
        return expr

    def leaf(self) -> Expr:
        if self.token.kind == "nam":
            var_name = self.token.text
            self.eat()
            return Var(var_name)
        elif self.token.kind == "int":
            val = int(self.token.text)
            self.eat()
            return Int(val)
        elif self.token.text == "(":
            self.eat()
            expr = self.expression()
            self.expect(")")
            return expr
        else:
            self.error()
