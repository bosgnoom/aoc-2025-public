import part1


def test_invalid_ids():
    assert part1.valid_id('55') == False
    assert part1.valid_id('6464') == False
    assert part1.valid_id('123123') == False


def test_start_zero():
    assert part1.valid_id('0101') == False
    assert part1.valid_id('101') == True
