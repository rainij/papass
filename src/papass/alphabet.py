import string
from collections.abc import Iterable
from functools import reduce

_preset_base = dict(
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

_preset_shortcuts = dict(
    all=list(_preset_base.keys()),
    letters=["lower", "upper"],
    special=["logogram", "punct", "quotes", "delim", "math", "braces"],
)


def alphabet_preset_base() -> dict[str, str]:
    """Map of names to a set of characters."""
    return _preset_base.copy()


def alphabet_preset_shortcuts() -> dict[str, list[str]]:
    """Map of shortcut names to names of sets of characters."""
    return _preset_shortcuts.copy()


def alphabet_from_preset(preset: Iterable[str]) -> str:
    """Create an alphabet from a preset.

    A *preset* is a list of names. Each name identifies a set of characters. The created
    alphabet is the union of all these sets.

    :param preset: The preset. Can contain duplicates.
    :return: A deduplicated and sorted string representing the alphabet.

    Example
    =======

    >>> alphabet_from_preset(["digits"])
    '0123456789'
    >>> alphabet_from_preset(["digits", "letters", "digits"])
    '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    """
    raw_names: list[str] = []

    for name in preset:
        if name in _preset_base:
            raw_names.append(name)
        elif name in _preset_shortcuts:
            raw_names.extend(_preset_shortcuts[name])
        else:
            raise AssertionError(
                f"Unknown alphabet preset component '{name}'. Choose from "
                + f"{_preset_base_join()} or use a shortcut: {_preset_shortcut_join()}."
            )

    raw_result = reduce(lambda a, n: a + _preset_base[n], raw_names, "")
    return "".join(sorted(set(raw_result)))


def _preset_base_join():
    return ",".join(_preset_base)


def _preset_shortcut_join():
    return ",".join(_preset_shortcuts)
