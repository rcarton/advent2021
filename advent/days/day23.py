import io
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Tuple, TextIO, Deque, Optional

Color = str

COSTS: Dict[Color, int] = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

# HABCD
Room = str

# Room, Room index
Pos = Tuple[Room, int]

# Cost, new pos, done
Move = Tuple[int, Pos]


def make_burrow_map(depth: int) -> Dict[Pos, List[Pos]]:
    bm = defaultdict(list)

    def connect(p1: Pos, p2: Pos):
        bm[p1].append(p2)
        bm[p2].append(p1)

    for i in range(1, 11):
        connect(('H', i), ('H', i - 1))
    connect(('H', 2), ('A', 0))
    connect(('H', 4), ('B', 0))
    connect(('H', 6), ('C', 0))
    connect(('H', 8), ('D', 0))

    for i in range(depth - 1):
        connect(('A', i), ('A', i + 1))
        connect(('B', i), ('B', i + 1))
        connect(('C', i), ('C', i + 1))
        connect(('D', i), ('D', i + 1))
    return bm


BURROW_MAP: Dict[int, Dict[Pos, List[Pos]]] = {
    2: make_burrow_map(2),
    4: make_burrow_map(4),
}


@dataclass(frozen=True, eq=True)
class Amphipod:
    color: Color
    pos: Pos
    done: bool = False

    def move_to(self, new_pos: Pos, done: bool = False) -> 'Amphipod':
        return Amphipod(
            color=self.color,
            pos=new_pos,
            done=done,
        )

    def as_done(self) -> 'Amphipod':
        return Amphipod(
            color=self.color,
            pos=self.pos,
            done=True,
        )


@dataclass(frozen=True, eq=True)
class State:
    cost: int
    pods: List[Amphipod]
    depth: int

    def get_pod_at_pos(self, p: Pos) -> Optional[Amphipod]:
        for pod in self.pods:
            if pod.pos == p:
                return pod
        return None

    def __hash__(self):
        sorted_pods = sorted(self.pods, key=lambda p: ord(p.color) * 1000 + ord(p.pos[0]) * 100 + p.pos[1])
        return hash(f"{self.cost}-{':'.join([str(hash(p)) for p in sorted_pods])}")

    def __repr__(self):
        burrow = {
            'H': ['.'] * 11,
            'A': ['.'] * self.depth,
            'B': ['.'] * self.depth,
            'C': ['.'] * self.depth,
            'D': ['.'] * self.depth,
        }
        for pod in self.pods:
            room, room_index = pod.pos
            burrow[room][room_index] = pod.color

        s = '#' * 13 + '\n'
        s += f"#{''.join(burrow['H'])}#\n"

        s += f"###{burrow['A'][0]}#{burrow['B'][0]}#{burrow['C'][0]}#{burrow['D'][0]}###\n"
        for i in range(1, self.depth):
            s += f"  #{burrow['A'][i]}#{burrow['B'][i]}#{burrow['C'][i]}#{burrow['D'][i]}#\n"
        s += f"  #########\n"

        return s

    @classmethod
    def from_string(cls, s: str, cost: int = 0, depth: int = 2):
        lines = s.strip().splitlines()
        pods = []
        for i, val in enumerate(lines[1][1:-1]):
            if val != '.':
                pods.append(Amphipod(color=val, pos=('H', i)))

        def add_pod(pos: Pos, line: int, column: int):
            val = lines[line][column]
            if val != '.':
                pods.append(Amphipod(color=val, pos=pos))

        for i in range(depth):
            add_pod(('A', i), 2 + i, 3)
            add_pod(('B', i), 2 + i, 5)
            add_pod(('C', i), 2 + i, 7)
            add_pod(('D', i), 2 + i, 9)

        state = cls(cost, pods, depth)
        for i, pod in enumerate(state.pods):
            if is_done(state, pod, pod.pos):
                state.pods[i] = pod.as_done()
        return state


def burrow_complete(state: State) -> bool:
    return all(pod.done for pod in state.pods)


def is_done(state: State, pod: Amphipod, pos: Pos) -> bool:
    """Return True if a pod is done if dropped at pos"""
    if pod.color != pos[0]:
        return False

    return set(p.pos[1] for p in state.pods if p.color == pos[0] and p.pos[0] == pos[0] and p.pos[1] > pos[1]) == set(
        range(pos[1] + 1, state.depth))


def legal_moves(state: State, pod_index: int, known_min: int = -1) -> List[Move]:
    """Return a list of possible moves for a pod."""
    pod = state.pods[pod_index]
    if pod.done:
        return []

    cost_per_move = COSTS[pod.color]

    # Find all accessible cells from the current cell
    visited = set(pod.pos)
    occupied = set(p.pos for p in state.pods)
    to_visit: Deque[Move] = deque([(cost_per_move, p) for p in BURROW_MAP[state.depth][pod.pos]])

    pod_room = pod.pos[0]

    valid: List[Move] = []
    while to_visit:
        cost, cp = to_visit.pop()

        if cp in visited or cp in occupied:
            # We can't go here
            continue

        visited.add(cp)

        # Bad path, not worth exploring
        if 0 < known_min <= state.cost + cost:
            continue

        current_room, current_index = cp

        # Can only go from a room to hallway or h to room
        if pod_room != current_room:
            if current_room == 'H':
                # Optim: can't go straight out of a room
                if current_index in (2, 4, 6, 8):
                    # Pass, we'd be right out of a room, blocking the door
                    pass
                else:
                    valid.append((cost, cp))

            if current_room == pod.color:
                # We can only put a pod in its room color if it's its last position
                if is_done(state, pod, cp):
                    # Optim: if one of the moves makes the pod done, it's the best move
                    return [(cost, cp)]

        to_visit.extend((cost + cost_per_move, p) for p in BURROW_MAP[state.depth][cp])

    return sorted(valid, key=lambda m: -m[0])


def parse_data(data: TextIO, depth: int = 2) -> State:
    return State.from_string(data.read(), depth=depth)


def legal_states(state: State, known_min: int = -1) -> List[State]:
    """Return a list of possible states given an existing state."""

    new_states = []
    for pod_index, pod in enumerate(state.pods):
        if pod.done:
            continue

        for cost, new_pos in legal_moves(state, pod_index, known_min):
            # Optimization: no need to keep going down this tree since we know it's going
            # to be more expensive
            if 0 < known_min <= state.cost + cost:
                continue

            new_states.append(State(
                state.cost + cost,
                state.pods[:pod_index] + [pod.move_to(new_pos, done=is_done(state, pod, new_pos))] + state.pods[
                                                                                                     pod_index + 1:],
                depth=state.depth,
            ))

    return new_states


def solve(initial_state: State) -> int:
    to_try: Deque[State] = deque([initial_state])
    min_value = -1

    attempted = set()

    while to_try:
        # Pop right would make it depth first, which is a good way to get a baseline min
        state = to_try.pop()

        if 0 < min_value <= state.cost:
            continue

        h = hash(state)
        if h in attempted:
            continue
        # assert h not in attempted
        attempted.add(h)

        # print(state)
        if burrow_complete(state):
            print(f"Solution found={state.cost}")
            min_value = state.cost if min_value == -1 else min(min_value, state.cost)
            continue
        to_try.extend(legal_states(state, min_value))

    return min_value


def first(data: TextIO) -> int:
    initial_state = parse_data(data, 2)
    return solve(initial_state)


def second(data: TextIO) -> int:
    data = data.read().strip()
    data = data.splitlines()
    data = data[:3] + [
        "  #D#C#B#A#",
        "  #D#B#A#C#",
    ] + data[3:]
    data = io.StringIO('\n'.join(data))
    initial_state = parse_data(data, 4)
    print(initial_state)
    return solve(initial_state)
