from typing import TextIO, Tuple, List, Set

# x, y
Pos = Tuple[int, int]
Dots = Set[Pos]
Fold = Pos


def parse_data(data: TextIO) -> Tuple[Dots, List[Fold]]:
    dots_s, folds_s = data.read().split('\n\n')
    dots: Dots = set([tuple(map(int, d.split(',', 2))) for d in dots_s.split()])

    folds = []
    for line in folds_s.split('\n'):
        if not line:
            continue

        y_or_x, num_s = line.split('=')
        if y_or_x[-1] == 'y':
            folds.append((0, int(num_s)))
        else:
            folds.append((int(num_s), 0))

    return dots, folds


def fold_paper(dots: Dots, fold: Fold) -> Dots:
    new_dots = set()
    fold_x, fold_y = fold
    for x, y in dots:
        new_x = x if (fold_x == 0 or x < fold_x) else fold_x - (x - fold_x)
        new_y = y if (fold_y == 0 or y < fold_y) else fold_y - (y - fold_y)
        new_dots.add((new_x, new_y))

    return new_dots


def first(data: TextIO) -> int:
    dots, folds = parse_data(data)
    dots = fold_paper(dots, folds[0])
    return len(dots)


def repr_dots(dots: Dots) -> str:
    xs, ys = zip(*dots)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    s = '\n'
    for y in range(min_y, max_y + 1):
        s += ''.join('#' if (x, y) in dots else '.' for x in range(min_x, max_x + 1))
        s += '\n'

    return s


def second(data: TextIO) -> int:
    dots, folds = parse_data(data)
    for fold in folds:
        dots = fold_paper(dots, fold)
    print(repr_dots(dots))

    return -1
