import pytest
from pathlib import Path
from day12 import read_input, get_those_who_fit
from day12_visual import day12_visual_sample


@pytest.fixture
def get_sample_input():
    # blocks, blocks_sizes, presents
    return read_input(Path('12/sample01.txt'))


def test_get_those_who_fit_nope(get_sample_input):
    _, blocks_sizes, _ = get_sample_input
    packing_list = ['2x2: 1 0 0 0 0 0',]
    assert get_those_who_fit(blocks_sizes, packing_list) == []


def test_get_those_who_fit_yep(get_sample_input):
    _, blocks_sizes, _ = get_sample_input
    packing_list = ['3x3: 0 1 0 0 0 0',]
    assert len(get_those_who_fit(blocks_sizes, packing_list)) == 1


def test_day12_visual_sample():
    assert day12_visual_sample('12/sample01.txt') == 2
