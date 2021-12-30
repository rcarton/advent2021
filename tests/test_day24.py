import io

import pytest

from days.day24 import first, second, parse_data, run, max_list_int, all_outputs
from utils import binseq_to_int

data = open("../data/day24.txt").read()

@pytest.fixture(name="section")
def get_section():
    dd = """
    inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
    instructions = parse_data(io.StringIO(dd))
    return instructions[0]

def test_parse_data():
    sections = parse_data(io.StringIO(data))
    assert len(sections) == 14

def test_run_instr(section):
    bits = '10101110'
    value = binseq_to_int(bits)
    vars = run(section, vars=dict(w=value))

    assert vars == {
        'w': int(bits[-4]),
        'x': int(bits[-3]),
        'y': int(bits[-2]),
        'z': int(bits[-1]),
    }

def test_run_instr_2(section):
    dd = """inp w
mul z 3
eql z x"""
    section = parse_data(io.StringIO(dd))[0]
    assert run(section, vars=dict(z=3, x=9))['z'] == 1
    assert run(section, vars=dict(z=3, x=8))['z'] == 0
    assert run(section, vars=dict(z=1, x=3))['z'] == 1


def test_run_instr_3():
    dd = """inp w
mul x 0
add x z
mod x 26
div z 26
add x -7
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y"""
    section = parse_data(io.StringIO(dd))[0]
    for z in range(100000):
        for w in range(1, 10):
            if run(section, vars=dict(z=z, w=w))['z'] == 0:
                print(w, z)
                assert False

@pytest.mark.parametrize("a, b, expected", [
    ([1,2,3], [1,2,4], [1,2,4]),
    ([4,2,3], [1,2,4], [4,2,3]),
])
def test_max_list_int(a, b, expected):
    assert max_list_int(a, b) == expected


def test_all_outputs(section):
    ao = all_outputs(section)
    ao = all_outputs(section, ao)
    assert ao == [([9, 9], 0), ([9, 8], 1)]


def test_first():
    assert first(io.StringIO(data)) == 739785


def test_second():
    assert second(io.StringIO(data)) == 444356092776315
