import pytest
import day11
from pathlib import Path


def test_part1(monkeypatch):
    monkeypatch.setattr(day11, "PLOTTING", False)
    assert day11.count_pathways(day11.read_input(Path('11/sample01.txt')), "you", "out") == 5


def test_part2(monkeypatch):
    monkeypatch.setattr(day11, "PLOTTING", False)

    # Testing count of all routes here, not only including dac and fft
    assert day11.count_pathways(day11.read_input(Path('11/sample02.txt')), "svr", "out") == 8


def test_day11_complete(monkeypatch):
    monkeypatch.setattr(day11, "PLOTTING", False)
    assert day11.run_all('11/sample01.txt', '11/sample02.txt') == (5, 2)
