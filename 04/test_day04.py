from pathlib import Path
from day04 import read_input, count_neighbours


def test_count_neighbours():
    puzzle = read_input(Path("04/sample01.txt"))

    assert len(count_neighbours(puzzle)) == 13
