import io
import itertools as it
from collections import defaultdict

from days.day19 import first, second, rotate_around_axis, rotate_to_orientation, all_orientations, parse_data, \
    overlap, calibrate_scanner, manhattan

data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""


def test_first():
    assert first(io.StringIO(data)) == 79


def test_second():
    assert second(io.StringIO(data)) == 3621


def rotate_pos(l, n: int):
    return l[n:] + l[:n]


def test_rotate_around():
    assert rotate_around_axis((4, 2, 5), 2) == (2, -4, 5)
    assert rotate_around_axis((0, 2, 1), 0) == (0, 1, -2)


def test_rotate_to_orientation():
    p = (5, 3, 7)
    # Rotating 4 times by 90deg == same thing
    assert rotate_to_orientation(p, (4, 0, 0)) == p
    assert rotate_to_orientation(p, (0, 4, 0)) == p
    assert rotate_to_orientation(p, (0, 0, 4)) == p
    assert rotate_to_orientation(p, (4, 4, 4)) == p

    expected = p
    expected = rotate_around_axis(expected, 0)
    expected = rotate_around_axis(expected, 0)
    expected = rotate_around_axis(expected, 1)
    expected = rotate_around_axis(expected, 2)
    expected = rotate_around_axis(expected, 2)
    expected = rotate_around_axis(expected, 2)
    assert rotate_to_orientation(p, (2, 1, 3)) == expected


def test_all_rotations():
    # it.permutations([0,1,2,3], 3) has 24, is this bueno?
    all_rot = list(it.product(*[list(range(4)) for _ in range(3)]))
    p = (5, 3, 7)

    r = defaultdict(list)
    for rot in all_rot:
        pp = rotate_to_orientation(p, rot)
        r[pp].append(rot)

    assert (len(set(all_orientations()))) == 24


def test_parse_data():
    scanners = parse_data(io.StringIO(data))
    assert len(scanners) == 5
    assert scanners[0].id == 0
    assert scanners[0].beacons[0] == (404, -588, -901)
    assert scanners[0].beacons[-1] == (459, -707, 401)
    assert scanners[4].beacons[2] == (441, 611, -461)


def test_overlap():
    scanners = parse_data(io.StringIO(data))
    assert overlap(scanners[0], scanners[1]) is not None


def test_calibrate_scanners():
    scanners = parse_data(io.StringIO(data))
    over = overlap(scanners[0], scanners[1])
    calibrate_scanner(scanners[0], scanners[1], over)
    assert scanners[0].pos == (0, 0, 0)
    assert scanners[1].pos == (68, -1246, -43)


def test_manhattan():
    assert manhattan((1105, -1205, 1229), (-92, -2380, -20)) == 3621
