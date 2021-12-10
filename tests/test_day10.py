import io

import pytest

from days.day10 import first, second, find_invalid_closing_character

data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


@pytest.mark.parametrize("line, expected", [
    ("{([(<{}[<>[]}>{[]{[(<()>", "}"),
    ("[[<[([]))<([[{}[[()]]]", ")"),
    ("[{[{({}]{}}([{[{{{}}([]", "]"),
    ("[<(<(<(<{}))><([]([]()", ")"),
    ("<{([([[(<>()){}]>(<<{{", ">"),
    ("[({(<(())[]>[[{[]{<()<>>", None),
])
def test_first_invalid_character(line, expected):
    assert find_invalid_closing_character(line) == expected


def test_first():
    assert first(io.StringIO(data)) == 26397


def test_second():
    assert second(io.StringIO(data)) == 288957
