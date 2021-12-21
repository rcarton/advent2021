from typing import TextIO, Iterator, List, Tuple, Dict, Optional


def parse_data(data: TextIO) -> List[int]:
    return [int(line.split(': ')[1]) for line in data.read().strip().splitlines()]


def ddie() -> Iterator[int]:
    i = 1
    while True:
        yield i
        i = i + 1 if i < 100 else 1


def ddie_sum() -> Iterator[int]:
    i = ddie()
    while True:
        yield next(i) + next(i) + next(i)


def first(data: TextIO) -> int:
    scores = [0, 0]
    pos = parse_data(data)
    current_player = 0

    roll_count = 0
    ddie_sum_iter = ddie_sum()
    while scores[0] < 1000 and scores[1] < 1000:
        pos[current_player] = (pos[current_player] + next(ddie_sum_iter) - 1) % 10 + 1
        scores[current_player] += pos[current_player]
        # print(f"Player {current_player+1} moves to space {pos[current_player]} for a total score of {scores[current_player]}.")
        roll_count += 3
        current_player = (current_player + 1) % 2

    # print(f"loser score={min(scores)} roll_count={roll_count}")
    return min(scores) * roll_count


# Probability for each sum of 3 rolls, instead of generating 27 universes, one for each combination
# of 3 die rolls, since we only use the sum of the rolls, we can use the 7 possible sums and
# how often they happen. for instance, the only way to roll 3, is to get 1+1+1
# To get the counts for each sum you can run this:
# Counter(list(sum(i) for i in it.product(*[(1,2,3)] *3)))
THREE_DIE_SUM_PROBA = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

Pos = int
Score = int
Player = Tuple[Pos, Score]
State = Tuple[Player, Player, int]


def is_winning(state: State) -> Optional[int]:
    """Return the index of the winning player or None if no winner"""
    for player in (0, 1):
        score = state[player][1]
        if score >= 21:
            return player
    return None


def get_new_state(state: State, dsum: int) -> State:
    """Apply the die sum to state and switch the current player."""
    current_player = state[2]
    other_player = state[(current_player + 1) % 2]
    pos, score = state[current_player]
    new_pos = (pos + dsum - 1) % 10 + 1
    new_score = score + new_pos
    new_player = (new_pos, new_score)

    return (new_player, other_player, 1) if current_player == 0 else (other_player, new_player, 0)


# Memoize the results since we're going to be computing the same win_counts a lot
CACHE: Dict[State, Tuple[int, int]] = {}


def win_counts(state: State) -> Tuple[int, int]:
    # We've already computed from this state
    if state in CACHE:
        return CACHE[state]

    # We need to compute the winning chances from here
    totals = [0, 0]
    for dice_sum, proba in THREE_DIE_SUM_PROBA.items():
        new_state = get_new_state(state, dice_sum)
        winning_player = is_winning(new_state)
        if winning_player is not None:
            totals[winning_player] += proba
        else:
            # No winner with this new state, keep recursing
            win0, win1 = win_counts(new_state)
            totals[0] += win0 * proba
            totals[1] += win1 * proba

    CACHE[state] = tuple(totals)
    return CACHE[state]


def second(data: TextIO) -> int:
    pos = parse_data(data)
    initial_state = ((pos[0], 0), (pos[1], 0), 0)
    wins = win_counts(initial_state)
    return max(wins)
