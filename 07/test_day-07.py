from day07 import main


def test_part1():
    part1, _ = main("07/sample01.txt")
    assert part1 == 21


def test_part2():
    _, part2 = main("07/sample01.txt")
    assert part2 == 40
