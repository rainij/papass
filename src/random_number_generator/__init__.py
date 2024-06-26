from typing import Type

from .base import RandomNumberGeneratorBase
from .dice import DiceRng
from .system import SystemRng

rngs: dict[str, tuple[Type[RandomNumberGeneratorBase], dict[str, str]]] = dict(
    system=(SystemRng, {}), dice=(DiceRng, {"num_sides": "dice_sides"})
)


def available_rngs() -> list[str]:
    return list(rngs.keys())


def get_rng(source: str, **possible_options):
    RngCls, args = rngs[source]
    return RngCls(**{kw: possible_options[o] for kw, o in args.items()})
