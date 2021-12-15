import itertools as it
from collections import Counter
from math import ceil
from typing import Dict, TextIO, Tuple

Template = str
Rules = Dict[str, str]


def parse_data(data: TextIO) -> Tuple[Template, Rules]:
    data = data.read()
    template_s, rules_list = data.split('\n\n')
    template = template_s.strip()
    rules = {r[0]: r[1] for r in [r.split(' -> ') for r in rules_list.split('\n') if r]}
    return template, rules


def insert(template: Template, rules: Rules) -> Template:
    new_template = ''
    for a, b in it.pairwise(template):
        new_template += a
        new_template += rules.get(a + b, '')
    new_template += template[-1]
    return new_template


def first(data: TextIO) -> int:
    template, rules = parse_data(data)

    for _ in range(10):
        template = insert(template, rules)

    counter = Counter(template)
    sorted_by_count = counter.most_common()

    return sorted_by_count[0][1] - sorted_by_count[-1][1]


def insert_2(counter: Counter[str], rules: Rules) -> Counter[str]:
    """Keeps counts of pairs, and breaks up each pair into two new pairs."""
    new_counter = Counter()
    for pair, count in counter.items():
        a, b = pair
        c = rules[a + b]
        new_counter[a + c] += count
        new_counter[c + b] += count
    return new_counter


def count_by_letter(counter: Counter[str]) -> Counter[str]:
    """Count the letters from a counter that counts pairs."""
    counter_by_letter = Counter()
    for pair, count in counter.items():
        a, b = pair
        counter_by_letter[a] += count / 2
        counter_by_letter[b] += count / 2

    # Round up for letters counted only "half" because they weren't in 2 pairs
    for pair, count in counter_by_letter.items():
        counter_by_letter[pair] = ceil(count)
    return counter_by_letter


def second(data: TextIO) -> int:
    template, rules = parse_data(data)

    counter = Counter(a + b for a, b in it.pairwise(template))

    for _ in range(40):
        counter = insert_2(counter, rules)
    sorted_by_count = count_by_letter(counter).most_common()

    return sorted_by_count[0][1] - sorted_by_count[-1][1]
