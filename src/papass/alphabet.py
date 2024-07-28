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


def alphabet_base_names() -> dict[str, str]:
    return _components.copy()


def alphabet_shortcuts() -> dict[str, list[str]]:
    return _shortcuts.copy()


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
                + f"{_base_names()}, or a shortcut {_shortcut_names()}."
            )

    return reduce(lambda a, n: a + _components[n], raw_names, "")


def _base_names():
    return ", ".join(f"'{n}'" for n in _components)


def _shortcut_names():
    return ", ".join(f"'{n}'" for n in _shortcuts)
