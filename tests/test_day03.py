from io import StringIO

from days.day03 import first, second, oxygen_generator_rating, co2_scrubber_rating

data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

data_list_ints = [list(map(int, i)) for i in data.splitlines()]


def test_first():
    assert first(StringIO(data)) == 198


def test_oxygen_generator_rating():
    assert oxygen_generator_rating(data_list_ints) == 23


def test_co2_scrubber_rating():
    assert co2_scrubber_rating(data_list_ints) == 10


def test_second():
    assert second(StringIO(data)) == 230
