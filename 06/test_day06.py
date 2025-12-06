from pathlib import Path
from day06 import read_input, part1, part2
import pytest


@pytest.fixture
def puzzle():
    return read_input(Path("06/sample01.txt"))


def test_part1(puzzle):
    assert part1(puzzle) == 4277556


def test_part2(puzzle):
    assert part2(Path("06/sample01.txt")) == 3263827
