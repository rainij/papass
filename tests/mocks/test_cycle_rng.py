from .cycle_rng import MockCycleRng


def test_cycle_rng():
    rng = MockCycleRng(range(10, 12))

    assert rng.randbelow(10) == 0
    assert rng.randbelow(10) == 1
    assert rng.randbelow(10) == 0
    assert rng.randbelow(10) == 1
