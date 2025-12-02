from day01 import calc_pos, main, read_input
from pathlib import Path


def test_R8():
    pos, _ = calc_pos(11, "R8")
    assert pos == 19


def test_L19():
    pos, _ = calc_pos(19, "L19")
    assert pos == 0


def test_L10():
    pos, _ = calc_pos(5, "L10")
    assert pos == 95

    pos, _ = calc_pos(pos, "R5")
    assert pos == 0


def test_sample1():
    assert main(read_input(Path('01/sample01.txt')), 1) == 3
