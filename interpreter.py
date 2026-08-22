"""
The bytecode interpreter. A stack machine.
"""

from bytecodes import ByteCode, Op


class CalcVm:
    def __init__(self):
        # The variables: names referencing integers.
        self.variables: dict[str, int] = {}
        # The stack: values in progress.
        self.stack: list[int] = []

    def execute(self, bytecode: list[ByteCode]) -> None:
        """Execute bytecode.

        Example each bytecode in turn, and do what it says.
        """
        for bc in bytecode:
            match bc:
                # Push an integer value onto the stack.
                case ByteCode(Op.PUSH_INT, value):
                    self.stack.append(value)

                # Pop a value from the stack and store it in a variable.
                case ByteCode(Op.STORE_VAR, var_name):
                    self.variables[var_name] = self.stack.pop()

                # Get the value of a variable and push it on the stack.
                case ByteCode(Op.LOAD_VAR, var_name):
                    self.stack.append(self.variables[var_name])

                # Pop two values off the stack, perform a binary operation on
                # them, and push the result back on the stack.
                case ByteCode(Op.BIN_OP, op):
                    right = self.stack.pop()
                    left = self.stack.pop()
                    match op:
                        case "+":
                            val = left + right
                        case "-":
                            val = left - right
                        case "*":
                            val = left * right
                        case "/":
                            val = left // right
                    self.stack.append(val)

                # Pop a value from the stack and print it.
                case ByteCode(Op.PRINT, _):
                    print(self.stack.pop())
