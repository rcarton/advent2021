import io

from days.day07 import first, second, fuel_cost, cost_to_move_crab

data = """16,1,2,0,4,2,7,1,2,14"""

crabs = [int(i) for i in data.split(',')]


def test_fuel_cost():
    assert fuel_cost(2, crabs) == 37
    assert fuel_cost(1, crabs) == 41
    assert fuel_cost(3, crabs) == 39
    assert fuel_cost(10, crabs) == 71


def test_cost_to_move_crab():
    assert cost_to_move_crab(16, 5) == 66
    assert cost_to_move_crab(1, 5) == 10
    assert cost_to_move_crab(1, 1) == 0


def test_first():
    assert first(io.StringIO(data)) == 37


def test_second():
    assert second(io.StringIO(data)) == 168
