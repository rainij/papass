import pytest
from papass import PassWordGenerator

from tests.utils.cycle_rng import CycleRng


class TestPassWordGenerator:
    @pytest.fixture
    def alphabet(self):
        alpha = "abcdefgh"
        assert len(alpha) == 2**3
        return alpha

    @pytest.mark.parametrize(
        "cycle, password",
        [
            ([2], "cccc"),
            ([0, 1], "abab"),
            ([0, 3, 1, 2], "adbc"),
            ([7, 4, 4, 6], "heeg"),
        ],
    )
    def test_uses_rng_choice_in_order(self, alphabet, cycle, password):
        pwg = PassWordGenerator(alphabet=alphabet, rng=CycleRng(cycle))
        result = pwg.generate(4)

        assert result.password == password
        assert result.entropy == pytest.approx(12.0)

    @pytest.mark.parametrize("length", range(4))
    def test_entropy(self, alphabet, length):
        pwg = PassWordGenerator(alphabet=alphabet, rng=CycleRng(range(4)))

        # alphabet has 8 characters, so 3 bits of entropy per character:
        assert pwg.generate(length).entropy == pytest.approx(3 * length)
