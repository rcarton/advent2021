from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Dict, TextIO, List, Iterator, Generic, TypeVar, Iterable, Tuple, Optional, Callable

from advent.utils import binseq_to_int

CounteratorT = TypeVar('CounteratorT')


class Counterator(Generic[CounteratorT]):
    """This is an iterator that also counts how many times next() has been called."""
    iterator: Iterator[CounteratorT]
    counter: int

    def __init__(self, iterable: Iterable[CounteratorT]):
        self.iterator = iter(iterable)
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self) -> CounteratorT:
        self.counter += 1
        return next(self.iterator)


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESSER_THAN = 6
    EQUAL = 7


@dataclass
class Packet:
    version: int
    type: PacketType
    value: Optional[int]
    sub_packets: List['Packet']

    def get_value(self):
        if self.type == PacketType.LITERAL:
            return self.value
        return OPS[self.type]([sp.get_value() for sp in self.sub_packets])


OPS: Dict[PacketType, Callable[[List[int]], int]] = {
    PacketType.SUM: sum,
    PacketType.PRODUCT: lambda v: reduce(lambda a, b: a * b, v, 1),
    PacketType.MINIMUM: min,
    PacketType.MAXIMUM: max,
    PacketType.GREATER_THAN: lambda v: 1 if v[0] > v[1] else 0,
    PacketType.LESSER_THAN: lambda v: 1 if v[0] < v[1] else 0,
    PacketType.EQUAL: lambda v: 1 if v[0] == v[1] else 0,
}


def hex_to_bit_list(data: str) -> List[int]:
    return list(map(int, ''.join([format(int(c, 16), 'b').zfill(4) for c in data.strip()])))


def chomp(source: Iterator[int], count: int) -> List[int]:
    return [next(source) for _ in range(count)]


def parse_literal_to_list(source: Counterator[int]) -> Tuple[List[int], int]:
    value = []
    count = 0
    while True:
        count += 1
        leading_bit = chomp(source, 1)[0]
        count += 4
        value += chomp(source, 4)
        if leading_bit == 0:
            break

    return value, count


def parse_literal(source: Counterator[int]) -> int:
    value = []
    while True:
        leading_bit = chomp(source, 1)[0]
        value += chomp(source, 4)
        if leading_bit == 0:
            break
    return binseq_to_int(value)


def parse_operator_sub_packets(source: Counterator[int]) -> List[Packet]:
    length_type_id = chomp(source, 1)[0]

    packets = []
    if length_type_id == 0:
        total_length = binseq_to_int(chomp(source, 15))

        count = 0
        while count < total_length:
            before = source.counter
            packets.append(parse_packet(source))
            count += source.counter - before
    else:
        sub_packet_count = binseq_to_int(chomp(source, 11))
        for _ in range(sub_packet_count):
            packets.append(parse_packet(source))

    return packets


def parse_packet(source: Counterator[int]) -> Packet:
    version = binseq_to_int(chomp(source, 3))
    type_id = binseq_to_int(chomp(source, 3))
    ptype = PacketType(type_id)

    value = None
    packets = []
    if ptype == PacketType.LITERAL:
        # Literal
        value = parse_literal(source)
    else:
        # Operator
        packets = parse_operator_sub_packets(source)

    return Packet(version=version,
                  type=ptype,
                  value=value,
                  sub_packets=packets)


def first(data: TextIO) -> int:
    bin_list = hex_to_bit_list(data.read().strip())
    packet = parse_packet(Counterator(bin_list))

    # Now flatten to get the sum of the versions
    total = 0
    packets = deque([packet])
    while packets:
        packet = packets.pop()
        total += packet.version
        packets.extend(packet.sub_packets)

    return total


def second(data: TextIO) -> int:
    bin_list = hex_to_bit_list(data.read().strip())
    packet = parse_packet(Counterator(bin_list))
    return packet.get_value()
