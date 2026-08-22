"""Parser for Calcium."""

from dataclasses import dataclass
from typing import Never

from tokenizer import Token


# The AST is an Abstract Syntax Tree. It represents the structure of the program
# as a tree of speciolized nodes.  For example, `1+2` a BinOp node with two
# children, both Int nodes.


@dataclass
class Ast:
    """The base class for any Ast node."""


@dataclass
class Expr(Ast):
    """A base class for any kind of expression."""


@dataclass
class Int(Expr):
    """An integer literal."""

    value: int


@dataclass
class Var(Expr):
    """A variable reference. Stores the name of the variable."""

    name: str


@dataclass
class BinOp(Expr):
    """A binary operator. Stores the operator (_-/*) and the right and left expressions."""

    op: str
    left: Expr
    right: Expr


@dataclass
class Stmt(Ast):
    """A base class for any statement."""


@dataclass
class Assign(Stmt):
    """An assignment statement, with a variable name and an expression."""

    var_name: str
    expr: Expr


@dataclass
class Print(Stmt):
    """A print statement, with the expression to print."""

    expr: Expr


@dataclass
class Program(Ast):
    """A complete program, a list of statements."""

    stmts: list[Stmt]


# Now for the parser itself. This is a "recursive descent" parser: methods
# represent the different structures in a program. Methods call each other to
# attempt to parse sub-structures.
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

    def expect(self, text) -> None:
        if self.token.text == text:
            self.eat()
        else:
            self.error(f"Expected {text!r}")

    def expect_kind(self, kind) -> None:
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
        expr = self.term()
        while self.token.text in {"*", "/"}:
            op = self.token.text
            self.eat()
            right = self.term()
            expr = BinOp(op, expr, right)
        return expr

    def term(self) -> Expr:
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
