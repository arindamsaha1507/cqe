"""Testing the index module."""

import pytest

from cqe.index import Index
from cqe.globs import IndexType


def test_index_passing():
    """Test the Index class."""
    Index(
        typ=IndexType.CLEAN,
        weight=0.5,
        category_limits=[0.1, 0.2, 0.3],
    )

    Index(
        typ=IndexType.FERTILITY,
        weight=0.5,
        category_limits=[0.3, 0.2, 0.1],
    )


def test_index_failing():
    """Test the Index class."""

    with pytest.raises(ValueError):
        Index(
            typ="clean",
            weight=0.5,
            category_limits=[0.1, 0.3, 0.2],
        )


def test_set_score_increasing():
    """Test the set_score method."""
    index = Index(
        typ="clean",
        weight=0.5,
        category_limits=[0.1, 0.2, 0.3],
    )
    index.set_score(0.05)
    assert index.score == 5.0

    index.set_score(0.15)
    assert index.score == 4.0

    index.set_score(0.25)
    assert index.score == 3.0

    index.set_score(0.35)
    assert index.score == 2.0
