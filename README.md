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
