from dataclasses import dataclass, replace
from typing import TextIO, Callable, Dict


@dataclass(frozen=True)
class Position:
    horizontal: int
    depth: int
    aim: int


UpdatePosFn = Callable[[Position, int], Position]


def up(pos: Position, value: int) -> Position:
    return replace(pos, depth=pos.depth - value)


def down(pos: Position, value: int) -> Position:
    return replace(pos, depth=pos.depth + value)


def forward(pos: Position, value: int) -> Position:
    return replace(pos, horizontal=pos.horizontal + value)


COMMANDS: Dict[str, UpdatePosFn] = {
    'up': up,
    'down': down,
    'forward': forward,
}


def up2(pos: Position, value: int) -> Position:
    return replace(pos, aim=pos.aim - value)


def down2(pos: Position, value: int) -> Position:
    return replace(pos, aim=pos.aim + value)


def forward2(pos: Position, value: int) -> Position:
    return replace(pos, horizontal=pos.horizontal + value, depth=pos.depth + pos.aim * value)


COMMANDS_v2: Dict[str, UpdatePosFn] = {
    'up': up2,
    'down': down2,
    'forward': forward2,
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
