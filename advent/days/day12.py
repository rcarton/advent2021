from collections import defaultdict, deque
from typing import TextIO, Dict, List, Set, Tuple, Deque, Optional

Graph = Dict[str, List[str]]


def parse_data(data: TextIO) -> Graph:
    g = defaultdict(list)
    for line in data.readlines():
        a, b = line.strip().split('-')
        g[a].append(b)
        g[b].append(a)

    return g


Path = List[str]
Visited = Set[str]
InProgress = Tuple[Path, Visited]


def is_lower(c: str) -> bool:
    return ord(c[0]) > ord('Z')


def first(data: TextIO) -> int:
    graph = parse_data(data)
    in_progress: Deque[InProgress] = deque([(['start'], {'start'})])
    complete: List[Path] = []

    while in_progress:
        path, visited = in_progress.pop()
        last_node = path[-1]
        neighbors = graph[last_node]
        for n in neighbors:
            if is_lower(n):
                if n in visited:
                    continue
                new_visited = visited | {n}
            else:
                new_visited = set(visited)

            new_path = path + [n]
            if n == 'end':
                complete.append(new_path)
            else:
                in_progress.append((new_path, new_visited))
    return len(complete)


Twice = Optional[str]
InProgress2 = Tuple[Path, Visited, Twice]


def can_be_visited(node: str, visited: Visited, twice: Twice) -> bool:
    if node == 'start':
        return False
    if node == 'end':
        return True

    if is_lower(node[0]):
        return node not in visited or twice is None
    return True


def second(data: TextIO) -> int:
    graph = parse_data(data)
    in_progress: Deque[InProgress2] = deque([(['start'], {'start'}, None)])
    complete: List[Path] = []

    while in_progress:
        path, visited, twice = in_progress.pop()
        last_node = path[-1]
        neighbors = graph[last_node]

        for n in neighbors:
            if not can_be_visited(n, visited, twice):
                continue

            new_path = path + [n]
            new_visited = set(visited)
            new_twice = twice
            if n == 'end':
                complete.append(new_path)
                continue

            if is_lower(n):
                if n in visited:
                    assert twice is None
                    new_twice = n
                else:
                    new_visited.add(n)

            in_progress.append((new_path, new_visited, new_twice))
    return len(complete)
