import string
from collections.abc import Iterable
from functools import reduce

_components = dict(
    lower=string.ascii_lowercase,
    upper=string.ascii_uppercase,
    digits=string.digits,
    logogram=r"#$%&@^~",
    punct=r".?!,:;",
    quotes="\"'`",
    delim=r"\/|_-",
    math=r"<>*+=",
    braces=r"{[()]}",
)

_shortcuts = dict(
    all=list(_components.keys()),
    letters=["lower", "upper"],
    special=["logogram", "punct", "quotes", "delim", "math", "braces"],
)


def alphabet_names():
    return ", ".join(f"'{n}'" for n in _components)


def alphabet_shortcut_names():
    return ", ".join(f"'{n}'" for n in _shortcuts)


def alphabet_from_charset_names(names: Iterable[str]) -> str:
    """TODO"""
    raw_names: list[str] = []

    for name in names:
        if name in _components:
            raw_names.append(name)
        elif name in _shortcuts:
            raw_names.extend(_shortcuts[name])
        else:
            raise AssertionError(
                f"Unknown alphabet name '{name}'. Choose one of "
                + f"{alphabet_names()}, or a shortcut {alphabet_shortcut_names()}."
            )

    return reduce(lambda a, n: a + _components[n], raw_names, "")
