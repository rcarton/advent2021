import io
import itertools as it
from collections import Counter

from days.day14 import first, second, parse_data, insert, count_by_letter

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def test_parse_data():
    template, rules = parse_data(io.StringIO(data))
    assert template == "NNCB"
    assert rules["HH"] == "N"
    assert len(rules.keys()) == 16


def test_count_by_letter():
    template, rules = parse_data(io.StringIO(data))
    for _ in range(10):
        template = insert(template, rules)
    counter = Counter(a + b for a, b in it.pairwise(template))
    result = count_by_letter(counter)
    assert result['B'] == 1749
    assert result['H'] == 161


def test_first():
    assert first(io.StringIO(data)) == 1588


def test_second():
    assert second(io.StringIO(data)) == 2188189693529
