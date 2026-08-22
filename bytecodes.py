"""
The byte codes for the Calcium virtual machine.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Op(Enum):
    """The opcodes (operations)."""

    # Pop a value from the stack and store it in a variable.
    STORE_VAR = auto()
    # Pop a value from the stack and print it.
    PRINT = auto()
    # Push an integer value onto the stack.
    PUSH_INT = auto()
    # Get the value of a variable and push it on the stack.
    LOAD_VAR = auto()
    # Pop two values off the stack, perform a binary operation on them,
    # and push the result back on the stack.
    BIN_OP = auto()


@dataclass
class ByteCode:
    """A bytecode has an operation and possibly a value to work on."""

    op: Op
    val: Any

    def __str__(self):
        if self.val is not None:
            return f"{self.op.name:10s} {self.val}"
        else:
            return self.op.name
