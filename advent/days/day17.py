from typing import TextIO, Tuple, List, Optional
import math
import itertools as it
import re

Velocity = Tuple[int, int]
Pos = Tuple[int, int]

# ((x_start, x_end), (y_start, y_end))
Target = Tuple[Tuple[int, int], Tuple[int, int]]

MAX_VY0 = 200
MAX_VX0 = 200


def y(vy0: int, t: int) -> int:
    return int(t / 2 * (2 * vy0 + (t - 1) * -1))


def x(vx0: int, t: int) -> int:
    # Time to speed = 0
    t = min(vx0, t)
    return int(t / 2 * (2 * vx0 + (t - 1) * -1))


def solve_quad_y(vy0: int, dest_y: int) -> float:
    """Finds the t at which the parabola intersents dest_y given an initial vy0"""

    a = -1 / 2
    b = (2 * vy0 + 1) / 2
    c = -dest_y
    discr = b ** 2 - 4 * (a * c)

    if discr < 0:
        raise Exception("no real solution")

    if discr > 0:
        #s1 = (-b + discr**.5)/(2*a)
        s2 = (-b - discr ** .5) / (2 * a)

        return s2

    return (-b + discr ** .5) / (2 * a)


def find_all_working_vy0s(dest_y1: int, dest_y2: int) -> List[Tuple[int, int]]:
    """Return a list of tuples (initial vy, t in target)"""
    if dest_y1 < dest_y2:
        dest_y1, dest_y2 = dest_y2, dest_y1

    results = []
    for v0 in range(-MAX_VY0, MAX_VY0):
        s1 = solve_quad_y(v0, dest_y1)
        s2 = solve_quad_y(v0, dest_y2)

        for i in range(math.ceil(s1), math.floor(s2)+1):
            results.append((v0, i))

    return results


def find_best_working_vx0(t: int, dest_x1: int, dest_x2: int) -> Optional[int]:
    """Return an initial v0 that works for this time t and the target"""
    results = []
    for v0 in range(MAX_VX0):
        val = x(v0, t)
        if val > dest_x2:
            break
        if dest_x1 < val < dest_x2:
            results.append(v0)

    if results:
        # Return the last one if more than one result, because it's the highest velocity, so it'll go higher
        return results[-1]

    return None


def find_all_working_vx0(t: int, dest_x1: int, dest_x2: int) -> List[int]:
    """Return an initial v0 that works for this time t and the target"""
    results = []
    for v0 in range(MAX_VX0):
        val = x(v0, t)
        if val > dest_x2:
            break
        if dest_x1 <= val <= dest_x2:
            results.append(v0)

    return results


def find_v0_with_biggest_vy0(target: Target) -> Velocity:
    working_vy0s = find_all_working_vy0s(*target[1])

    # Reverse it to start from the highest vy0s
    working_vy0s = list(reversed(working_vy0s))

    # print(working_vy0s)

    # Try to find a vx0 that ends up in the range
    for vy0, t in working_vy0s:
        vx0 = find_best_working_vx0(t, *target[0])
        if vx0:
            # print(pos((vx0, vy0), t))
            return vx0, vy0

    raise Exception("No value found")


def find_all_working_velocities(target: Target) -> List[Velocity]:
    working_vy0s = find_all_working_vy0s(*target[1])

    # Reverse it to start from the highest vy0s
    working_vy0s = list(reversed(working_vy0s))

    # print(working_vy0s)
    results = []

    # Try to find vx0s that end up in the target
    for vy0, t in working_vy0s:
        results += it.product(find_all_working_vx0(t, *target[0]), [vy0])

    # Dedup
    return list(set(results))


def find_apex(vy: int) -> int:
    apex = y(vy, 0)
    t = 0
    while True:
        t += 1
        val = y(vy, t)
        if val <= apex:
            return apex
        apex = val


def pos(v0: Velocity, t: int) -> Pos:
    return x(v0[0], t), y(v0[1], t)


def parse_data(data: TextIO) -> Target:
    a, b, c, d = list(map(int, re.findall(r"[-\d]+", data.read().strip())))
    return (a, b), (c, d)


def first(data: TextIO) -> int:
    target = parse_data(data)

    _, vy = find_v0_with_biggest_vy0(target)

    return find_apex(vy)


def second(data: TextIO) -> int:
    target = parse_data(data)
    all_velocities = find_all_working_velocities(target)

    return len(all_velocities)
