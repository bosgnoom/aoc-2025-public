import pytest
from pathlib import Path
from day09 import read_input, area, part1, part2

cases = {
    "a": ([[2, 5], [9, 7]], 24),
    "b": ([[7, 1], [11, 7]], 35),
    "c": ([[7, 3], [2, 3]], 6),
    "d": ([[2, 5], [11, 1]], 50),
}


@pytest.mark.parametrize("test_id, test_data", cases.items())
def test_area(test_id, test_data):
    coords, expected = test_data
    assert area(coords[0], coords[1]) is expected


@pytest.fixture
def puzzle():
    return read_input(Path("09/sample01.txt"))


def test_part1(puzzle):
    assert part1(puzzle) == 50


def test_part2(puzzle):
    assert part2(puzzle) == 24
