"""
The AST is an Abstract Syntax Tree. It represents the structure of the program
as a tree of specialized nodes.  For example, `1+2` a BinOp node with two
children, both Int nodes.
"""

from dataclasses import dataclass


@dataclass
class AstNode:
    """The base class for any Ast node."""


@dataclass
class Expr(AstNode):
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
class Stmt(AstNode):
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
class Program(AstNode):
    """A complete program, a list of statements."""

    stmts: list[Stmt]
