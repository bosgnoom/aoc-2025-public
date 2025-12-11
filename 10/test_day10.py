# Now for my own tests:
from pathlib import Path
import pytest
from part1 import minimal_flips
from part2 import solve_joltage, sample
import day10

examples = {
    # case: machine lights,
    #       buttons,
    #       joltage,
    #       answer for part1, part2

    "first": [[0, 1, 1, 0],
              [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]],
              [3, 5, 4, 7],
              2, 10],
    "second": [[0, 0, 0, 1, 0],
               [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]],
               [7, 5, 12, 7, 2],
               3, 12],
    "third": [[0, 1, 1, 1, 0, 1],
              [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]],
              [10, 11, 11, 5, 10, 5],
              2, 11],
}


@pytest.mark.parametrize("test_id, test_data", examples.items())
def test_examples_part1(test_id, test_data):
    # unpack examples
    lights, buttons, _, answer, _ = test_data
    assert minimal_flips(lights, buttons) == answer


@pytest.mark.parametrize("test_id, test_data", examples.items())
def test_examples_part2(test_id, test_data):
    # unpack examples
    _, buttons, joltage, _, answer = test_data
    assert sum(solve_joltage(joltage, buttons)) == answer


@pytest.fixture
def puzzle():
    return day10.read_input(Path("10/sample01.txt"))


def test_part1(puzzle):
    assert day10.part1(puzzle) == 7


def test_part2_sample():
    assert sample() == 10


def test_part2(puzzle):
    assert day10.part2(puzzle) == 33
