import pytest
from rspass.random.base import RandomNumberGeneratorBase

from tests.mocks.cycle_rng import MockCycleRng


class TestRandomNumberGeneratorBase:
    @pytest.fixture
    def cycle(self) -> list[int]:
        return [0, 3, 2, 1]

    @pytest.fixture(scope="class")
    def rng_class(self) -> RandomNumberGeneratorBase:
        return MockCycleRng([0, 3, 2, 1])

    @pytest.mark.parametrize("i", range(4))
    def test_choice_uses_randbelow_as_desired(self, i, cycle, rng_class):
        items = [10, 11, 12, 13]
        assert rng_class.choice(items) == items[cycle[i]]
