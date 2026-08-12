# Calcium

A micro-minimalist language, with an AST, "bytecode" and a virtual machine.

It's called calcium because it's pretty much just a simple calculator.

## Syntax

- There are only two statements: variable assignment and `print`.
- The only values are integers.
- The only operations are binary `+`, `-`, `*`, and `/`, with their usual precedence.
- Expressions can be parenthesized.
- The `print` statement only accepts a single expression.
- There are no comments.

## Example

```
x = 1
y = x + 10
z = 2 * (y + x)
print z
x = x + 100
print x
print x * z
```

## Running

Run `calcium.py` with a file name of a .calc file. It will show the parsed AST, the compiled byte code, and then execute the program.

```
% python3 calcium.py example.calc

=== AST =======================
Program(stmts=[Assign(var_name='x', expr=Int(value=1)),
               Assign(var_name='y',
                      expr=BinOp(op='+',
                                 left=Var(name='x'),
                                 right=Int(value=10))),
               Assign(var_name='z',
                      expr=BinOp(op='*',
                                 left=Int(value=2),
                                 right=BinOp(op='+',
                                             left=Var(name='y'),
                                             right=Var(name='x')))),
               Print(expr=Var(name='z')),
               Assign(var_name='x',
                      expr=BinOp(op='+',
                                 left=Var(name='x'),
                                 right=Int(value=100))),
               Print(expr=Var(name='x')),
               Print(expr=BinOp(op='*',
                                left=Var(name='x'),
                                right=Var(name='z')))])

=== Byte code =================
PUSH_INT   1
STORE_VAR  x
LOAD_VAR   x
PUSH_INT   10
BIN_OP     +
STORE_VAR  y
PUSH_INT   2
LOAD_VAR   y
LOAD_VAR   x
BIN_OP     +
BIN_OP     *
STORE_VAR  z
LOAD_VAR   z
PRINT
LOAD_VAR   x
PUSH_INT   100
BIN_OP     +
STORE_VAR  x
LOAD_VAR   x
PRINT
LOAD_VAR   x
LOAD_VAR   z
BIN_OP     *
PRINT

=== Execute ===================
24
101
2424
```
