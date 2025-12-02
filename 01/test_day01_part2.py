from day01 import calc_pos2, main, read_input
from pathlib import Path


def test_R8():
    pos, clicks = calc_pos2(50, "L68")
    assert pos == 82
    assert clicks == 1


def test_R1000():
    pos, clicks = calc_pos2(50, "R1000")
    assert pos == 50
    assert clicks == 10


def test_zero_R():
    pos, clicks = calc_pos2(0, "R100")
    assert pos == 0
    assert clicks == 1


def test_zero_L():
    pos, clicks = calc_pos2(0, "L100")
    assert pos == 0
    assert clicks == 1


def test_sample1():
    assert main(read_input(Path('01/sample01.txt')), 2) == 6
