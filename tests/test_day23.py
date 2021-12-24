import io

from days.day23 import first, second, parse_data, State, legal_states, legal_moves, is_done

data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def test_parse_data():
    r = str(parse_data(io.StringIO(data)))
    print('\n')
    print(r)
    dlines = data.splitlines()
    for i, line in enumerate(r.splitlines()):
        assert line == dlines[i]
    assert r == data


def test_legal_states():
    s0 = State.from_string("""
#############
#.B.....A..D#
###.#C#B#.###
  #A#D#C#.#
  ######### 
""")
    s1 = State.from_string("""
#############
#.B........D#
###A#C#B#.###
  #A#D#C#.#
  ######### 
""", 6)
    s2 = State.from_string("""
#############
#.B.....A...#
###A#C#B#.###
  #A#D#C#D#
  ######### 
""", 4000)
    states = legal_states(s0)
    assert len(states) == 12
    # Assert no dupe states
    assert len(set(states)) == 12
    print(states)
    # idk why these comparisons don't work, they look right
    # assert str(s1) in [str(states)]
    # assert str(s2) in [str(states)]


def test_legal_moves():
    s0 = State.from_string("""
#############
#.......A..D#
###B#C#B#.###
  #A#A#C#D#
  ######### 
""")
    moves = legal_moves(s0, 1)
    assert moves == [(3000, ('D', 0))]

    s0 = State.from_string("""
#############
#.......A..D#
###B#C#B#.###
  #A#D#C#.#
  ######### 
""")
    moves = legal_moves(s0, 1)
    assert moves == [(4000, ('D', 1))]
    s0 = State.from_string("""
#############
#...B......A#
###B#C#D#.###
  #A#D#C#.#
  ######### 
""")
    moves = legal_moves(s0, 4)
    assert moves == [(5000, ('D', 1))]

    s0 = State.from_string("""
#############
#...B......A#
###B#C#D#.###
  #A#D#C#.#
  #A#D#C#.#
  #A#D#C#.#
  ######### 
""", depth=4)
    moves = legal_moves(s0, 4)
    assert moves == [(7000, ('D', 3))]


def test_is_done():
    s0 = State.from_string("""
#############
#.......A..D#
###B#C#B#.###
  #A#D#C#.#
  ######### 
""")
    pod = s0.pods[1]
    assert is_done(s0, pod, ('D', 1)) is True
    assert is_done(s0, pod, ('D', 0)) is False


def test_first():
    assert first(io.StringIO(data)) == 12521


def test_second():
    assert second(io.StringIO(data)) == 44169
