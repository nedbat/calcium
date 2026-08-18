"""
Calcium's tokenizer.

The tokenizer takes plain text and produces a series of identified tokens.
Each token has a kind (keyword, punctuation, name, and so on), and the text of
the token.
"""

import re
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Token:
    """Each token has a kind and the text."""

    kind: str
    text: str

    def __str__(self):
        return f"{self.kind}: {self.text!r}"


# We use a regular expression (regex) to find the token patterns in the
# source code. This is a VERBOSE regex, enabled by the (?x) flag.
# Comments and whitespace are allowed and ignored in a verbose regex.
TOKENS = r"""(?mx)
    # There's only one keyword: "print":
    (?P<key>print)                                                          |

    # We have a few characters of punctuation:
    (?P<pnc>[-+*/()=])                                                      |

    # A name starts with a letter, then can continue with letters, digits, or
    # underscore:
    (?P<nam>[A-Za-z][A-Za-z0-9_]*)                                          |

    # An integer is any number of decimal digits:
    (?P<int>[0-9]+)                                                         |

    # The ends of lines are a token of their own:
    (?P<eol>$)                                                              |

    # We skip over whitespace and don't keep it:
    \s+                                                                     |

    # Anything else we find we'll consider an error:
    (?P<err>.)
    """


def tokenize(text: str) -> Iterator[Token]:
    """The tokenizer: use the TOKENS regex to find matches and yield tokens."""
    for m in re.finditer(TOKENS, text):
        if m.lastgroup:
            yield Token(m.lastgroup, m.group())
