import papass.random_source.registry
import pytest
from papass.random_source.registry import (
    available_random_sources,
    default_randomness_source,
    get_rng,
)

from tests.utils.cycle_rng import CycleRng


def test_default_random_source():
    assert default_randomness_source()


def test_available_random_sources():
    assert len(available_random_sources()) >= 2


@pytest.mark.parametrize("random_source,options", [("cycle_rng", dict(cycle_from_cmd=[0, 1]))])
def test_get_rng(monkeypatch, random_source, options):
    monkeypatch.setattr(
        papass.random_source.registry,
        "_rng_registry",
        dict(cycle_rng=(CycleRng, {"cycle": "cycle_from_cmd"})),
    )

    rng = get_rng(random_source, **options)

    assert isinstance(rng, CycleRng)
    assert [0, 1] == [rng.randbelow(2) for _ in range(2)]
