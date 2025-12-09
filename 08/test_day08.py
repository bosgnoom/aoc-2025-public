from day08 import read_input, coords_to_distances, part1, part2
import pytest
from pathlib import Path


@pytest.fixture()
def coords_sample():
    return read_input(Path("08/sample01.txt"))


@pytest.fixture()
def distances_sample(coords_sample):
    return coords_to_distances(coords_sample)


@pytest.fixture()
def coords():
    return read_input(Path("08/input.txt"))


@pytest.fixture()
def distances(coords):
    return coords_to_distances(coords)


def test_part1_sample(coords_sample, distances_sample):
    assert part1(coords_sample, distances_sample, 10) == 40


def test_part2_sample(coords_sample, distances_sample):
    assert part2(coords_sample, distances_sample) == 25272


def test_part1(coords, distances):
    assert part1(coords, distances, 1000) == 79056


def test_part2(coords, distances):
    assert part2(coords, distances) == 4639477
