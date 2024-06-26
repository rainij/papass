from typing import Type

from .base import RandomNumberGeneratorBase
from .dice import DiceRng
from .system import SystemRng

rng_registry: dict[str, tuple[Type[RandomNumberGeneratorBase], dict[str, str]]] = dict(
    # This maps the random_source to two things:
    # 1. A ctor for an rng.
    # 2. A dict mapping the __init__ options of the rng to their corresponding command line options.
    #
    # The first entry of this dict (dicts are ordered by insertion order) can be used as
    # the default of the command line tool.
    system=(SystemRng, {}),
    dice=(DiceRng, {"num_sides": "dice_sides"}),
)


def available_random_sources() -> list[str]:
    """Get a list of all valid values for --random-source."""
    return list(rng_registry.keys())


def get_rng(source: str, **possible_options):
    """Get a random number generator of the given source.

    The `possible_options` should contain all command line options which are relevant for
    the random_source. It is OK if it contains superfluous options which are not relevant
    to the rng (those are ignored)
    """
    RngCls, args = rng_registry[source]
    return RngCls(**{kw: possible_options[o] for kw, o in args.items()})
