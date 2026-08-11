from compiler import ByteCode


class CalcVm:
    def __init__(self):
        self.variables: dict[str, int] = {}
        self.stack: list[int] = []

    def execute(self, bytecode: list[ByteCode]) -> None:
        for bc in bytecode:
            match bc:
                case ByteCode("PUSH_INT", value):
                    self.stack.append(value)

                case ByteCode("STORE_VAR", var_name):
                    self.variables[var_name] = self.stack.pop()

                case ByteCode("LOAD_VAR", var_name):
                    self.stack.append(self.variables[var_name])

                case ByteCode("BIN_OP", op):
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

                case ByteCode("PRINT", _):
                    print(self.stack.pop())
