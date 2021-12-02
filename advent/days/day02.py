from dataclasses import dataclass, replace
from typing import TextIO, Callable, Dict


@dataclass(frozen=True)
class Position:
    horizontal: int
    depth: int
    aim: int


UpdatePosFn = Callable[[Position, int], Position]

COMMANDS: Dict[str, UpdatePosFn] = {
    'up': lambda pos, value: replace(pos, depth=pos.depth - value),
    'down': lambda pos, value: replace(pos, depth=pos.depth + value),
    'forward': lambda pos, value: replace(pos, horizontal=pos.horizontal + value),
}

COMMANDS_v2: Dict[str, UpdatePosFn] = {
    'up': lambda pos, value: replace(pos, aim=pos.aim - value),
    'down': lambda pos, value: replace(pos, aim=pos.aim + value),
    'forward': lambda pos, value: replace(pos, horizontal=pos.horizontal + value, depth=pos.depth + pos.aim * value),
}


def first(data: TextIO) -> int:
    pos = Position(horizontal=0, depth=0, aim=0)

    for instruction in data:
        cmd_s, value_s = instruction.split(' ')
        pos = COMMANDS[cmd_s](pos, int(value_s))

    return pos.depth * pos.horizontal


def second(data: TextIO) -> int:
    pos = Position(horizontal=0, depth=0, aim=0)

    for instruction in data:
        cmd_s, value_s = instruction.split(' ')
        pos = COMMANDS_v2[cmd_s](pos, int(value_s))

    return pos.depth * pos.horizontal
