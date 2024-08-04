import pytest
from papass.random_source.base import RngBase

from tests.utils.cycle_rng import CycleRng


def get_cycle() -> list[int]:
    return [0, 3, 2, 1]


class TestRandomNumberGeneratorBase:
    @pytest.fixture(scope="class")
    def cycle_rng(self) -> RngBase:
        return CycleRng(get_cycle())

    @pytest.mark.parametrize("i", range(4))
    def test_choice_uses_randbelow_as_desired(self, i, cycle_rng):
        items = [10, 11, 12, 13]
        cycle = get_cycle()

        assert cycle_rng.choice(items) == items[cycle[i]]
