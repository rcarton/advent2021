import io
from typing import List

import pytest

from days.day16 import parse_packet, hex_to_bit_list, parse_literal, PacketType, Counterator, first, second

data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@pytest.mark.parametrize("hex, version, packet_type, values", [
    ("38006F45291200", 1, PacketType.LESSER_THAN, [10, 20]),
    ("EE00D40C823060", 7, PacketType.MAXIMUM, [1, 2, 3]),
])
def test_parse_packet(hex: str, version: int, packet_type: PacketType, values: List[int]):
    source = hex_to_bit_list(hex)
    packet = parse_packet(Counterator(source))
    assert packet.version == version
    assert packet.type == packet_type


def test_parse_literal():
    assert parse_literal(Counterator(map(int, "101111111000101"))) == 2021


@pytest.mark.parametrize("hex, expected", [
    ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
    ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000"),
])
def test_hex_to_bit_list(hex, expected):
    assert hex_to_bit_list(hex) == list(
        map(int, expected))


def test_first():
    assert first(io.StringIO("a0016c880162017c3686b18a3d4780")) == 31


@pytest.mark.parametrize("hex, expected", [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
])
def test_second(hex, expected):
    assert second(io.StringIO(hex)) == expected
