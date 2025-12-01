import part1
from pathlib import Path


def test_R8():
    pos, _ = part1.calc_pos(11, "R8")
    assert pos == 19


def test_L19():
    pos, _ = part1.calc_pos(19, "L19")
    assert pos == 0


def test_L10():
    pos, _ = part1.calc_pos(5, "L10")
    assert pos == 95

    pos, _ = part1.calc_pos(pos, "R5")
    assert pos == 0


def test_sample1():
    assert part1.main(
        part1.read_input(Path('01/sample01.txt'))
    ) == 3
