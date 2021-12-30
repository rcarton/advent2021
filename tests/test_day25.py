import io

from days.day25 import first, second

data = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""


def test_first():
    assert first(io.StringIO(data)) == 58


def test_second():
    assert second(io.StringIO(data)) == 444356092776315
