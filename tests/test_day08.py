import io

from days.day08 import first, second, parse_data, SegmentPuzzle, translate_output

data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def test_parse_data():
    entries = list(parse_data(io.StringIO(data)))
    displays, h = entries[0]
    assert len(displays) == 10
    assert h == [set('fdgacbe'), set('cefdb'), set('cefbgd'), set('gcbe')]


def assert_list_equals(l1: list, l2: list) -> None:
    assert len(l1) == len(l2)
    for el in l1:
        assert el in l2


def test_get_possible_solutions():
    candidates = {
        'a': set('1'),
        'b': set('23'),
        'c': set('45')
    }
    expected = [
        {'a': '1', 'b': '2', 'c': '4'},
        {'a': '1', 'b': '2', 'c': '5'},
        {'a': '1', 'b': '3', 'c': '4'},
        {'a': '1', 'b': '3', 'c': '5'},
    ]
    assert_list_equals(SegmentPuzzle.get_possible_solutions(candidates, {}), expected)


def test_translate_output():
    digits, output = list(parse_data(io.StringIO(data)))[0]
    mapping = SegmentPuzzle(digits, output).solve()
    assert translate_output(output, mapping) == 8394


def test_first():
    assert first(io.StringIO(data)) == 26


def test_second():
    assert second(io.StringIO(data)) == 61229
