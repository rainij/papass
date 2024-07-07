import pytest
from rspass.random.base import RandomNumberGeneratorBase

from tests.utils.cycle_rng import CycleRng


class TestRandomNumberGeneratorBase:
    @pytest.fixture
    def cycle(self) -> list[int]:
        return [0, 3, 2, 1]

    @pytest.fixture(scope="class")
    def cycle_rng(self) -> RandomNumberGeneratorBase:
        return CycleRng([0, 3, 2, 1])

    @pytest.mark.parametrize("i", range(4))
    def test_choice_uses_randbelow_as_desired(self, i, cycle, cycle_rng):
        items = [10, 11, 12, 13]
        assert cycle_rng.choice(items) == items[cycle[i]]
