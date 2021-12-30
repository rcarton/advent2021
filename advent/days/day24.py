from collections import defaultdict
from typing import Tuple, List, Dict, TextIO, cast, Optional, DefaultDict, Union, Literal

# For each section of the program, x=0, y=0, only the values of z and w matter


# run a section, get the possible values out of the section
# if multiple input numbers get the same output value, keep the highest input (w)
# number only

Op = str
Value = str
Vars = Dict[str, int]
Instr = Tuple[Op, Value]
Section = List[Instr]

OPS = {
    'div': lambda a, b: a // b,
    'mul': lambda a, b: a * b,
    'add': lambda a, b: a + b,
    'mod': lambda a, b: a % b,
    'eql': lambda a, b: int(a == b),
}


def run(instructions: Section, vars: Optional[Vars] = None) -> Vars:
    vars = vars if vars else {}
    vars = {c: vars.get(c, 0) for c in 'wxyz'}

    for i in instructions:
        op, a, b = i
        if b in 'wxyz':
            b = vars[b]
        else:
            b = int(b)
        vars[a] = OPS[op](vars[a], b)

    return vars


def parse_data(data: TextIO) -> List[Section]:
    sections_s = data.read().strip().split('inp w\n')[1:]
    sections = []
    for section_s in sections_s:
        sections.append([tuple(line.split(' ')) for line in section_s.strip().splitlines()])
    return cast(List[Section], sections)


def min_list_int(a: List[int], b: List[int]) -> List[int]:
    return b if max_list_int(a, b) == a else a


def max_list_int(a: List[int], b: List[int]) -> List[int]:
    if len(a) > len(b):
        return a
    if len(b) > len(a):
        return b
    for a1, b1 in zip(a, b):
        if a1 == b1:
            continue
        return a if a1 > b1 else b
    return a


# ([<previous inp>,]
PrevWs = List[int]
Output = Tuple[PrevWs, int]


def all_outputs(section: Section, prev: Optional[List[Output]] = None) -> List[Output]:
    outputs: Dict[int, PrevWs] = {}

    if not prev:
        prev: Output = [([], 0)]

    for n in range(1, 10):
        for previous_ws, z in prev:
            vars = run(section, dict(w=n, z=z))
            ws = previous_ws + [n]
            if vars['z'] in outputs:
                outputs[vars['z']] = min_list_int(outputs[vars['z']], ws)
            else:
                outputs[vars['z']] = ws

    return [(prev_ws, z) for z, prev_ws in outputs.items()]


# def solve(section: Section):
# z == 1

Thing = Union['Function', 'Symbol', int]


class Function:
    op: str
    left: 'Symbol'
    right: Thing


class Symbol:
    name: str
    value: Thing


# def simplify(f: Function, symbols: Dict[str, int]) -> Thing:
#
#     left = f.left.value
#     if f.op == 'div':
#         assert f.right != 0
#         if f.right == 1:
#             return f.left
#         if type(f.left) == 'int':
#             return f.left // f.
#     elif f.op == 'mod':
#         assert f.right != 0
#         if f.right == 1:
#             return f.left
#     elif f.op == 'mul':
#         if f.right == 0:
#             return 0
#         if f.right == 1:
#             return f.left

def first(data: TextIO) -> int:
    sections = parse_data(data)
    ao = None
    for i, s in enumerate(sections):
        print(f"Section {i + 1}/14")
        ao = all_outputs(s, ao)

    mv = None
    for ws, z in ao:
        if z == 0:
            mv = min_list_int(mv, ws) if mv is not None else ws
            print(mv)
    return int(''.join([str(n) for n in mv]))


def second(data: TextIO) -> int:
    return -1
