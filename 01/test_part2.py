import part1
import part2
from pathlib import Path


def test_R8():
    pos, clicks = part2.calc_pos(50, "L68")
    assert pos == 82
    assert clicks == 1


def test_R1000():
    pos, clicks = part2.calc_pos(50, "R1000")
    assert pos == 50
    assert clicks == 10


def test_sample1():
    assert part2.main(
        part1.read_input(Path('01/sample01.txt'))
    ) == 6
