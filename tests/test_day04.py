import io

from days.day04 import first, second, parse_data

data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def test_parse_data():
    drawn, boards = parse_data(io.StringIO(data))
    assert drawn[:3] == [7, 4, 9]
    assert len(boards) == 3
    assert boards[1].rows[2] == {19, 8, 7, 25, 23}
    assert boards[1].columns[4] == {22, 5, 23, 4, 6}


def test_first():
    assert first(io.StringIO(data)) == 4512


def test_second():
    assert second(io.StringIO(data)) == 1924
