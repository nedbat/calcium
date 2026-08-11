import re
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Token:
    kind: str
    text: str

    def __str__(self):
        return f"{self.kind}: {self.text!r}"


TOKENS = r"""(?x)
    (?P<key>print)                      |
    (?P<pnc>[-+*/()=])                  |
    (?P<var>[A-Za-z][A-Za-z0-9_]*)      |
    (?P<int>[0-9]+)                     |
    (?P<eol>$)                          |
    \s+                                 |
    (?P<err>.)
    """


def tokenize(text: str) -> Iterator[Token]:
    for m in re.finditer(TOKENS, text):
        if m.lastgroup:
            yield Token(m.lastgroup, m.group())
