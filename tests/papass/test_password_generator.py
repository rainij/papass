import pytest
from papass import PassWordGenerator

from tests.utils.cycle_rng import CycleRng


class TestPassWordGenerator:

    @pytest.fixture
    def alphabet(self):
        return "abcd"

    @pytest.mark.parametrize("cycle, password", [
        ([2], "cccc"),
        ([0, 1], "abab"),
        ([0, 3, 1, 2], "adbc"),
    ])
    def test_uses_rng_choice_in_order(self, alphabet, cycle, password):
        pwg = PassWordGenerator(alphabet=alphabet, rng=CycleRng(cycle))
        result = pwg.generate(4)

        assert result.password == password
        assert result.entropy == pytest.approx(8.0)
